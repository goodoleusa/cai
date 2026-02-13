"""
SMS-Gate webhook receiver with blockchain timestamping.

Receives inbound SMS, computes SHA-256 hash, submits to OpenTimestamp,
stores evidence in PostgreSQL, and forwards event to OpenClaw.

Requires: flask, requests, psycopg2-binary
Env: OPENCLAW_URL, OPENCLAW_TOKEN, DATABASE_URL
"""

import hashlib
import json
import os

import requests
from flask import Flask, abort, request

try:
    import psycopg2
except ImportError:
    psycopg2 = None

app = Flask(__name__)

OPENCLAW_URL = os.getenv("OPENCLAW_URL")
OPENCLAW_TOKEN = os.getenv("OPENCLAW_TOKEN")
OTS_ENDPOINT = "https://api.opentimestamps.org/v1/timestamp"
DB_DSN = os.getenv("DATABASE_URL")


def canonical_hash(sms_payload: dict) -> tuple[str, str]:
    """
    Build a deterministic string from the SMS payload and hash it.
    """
    payload_inner = sms_payload.get("payload", {})
    relevant = {
        "deviceId": sms_payload.get("deviceId"),
        "messageId": payload_inner.get("messageId"),
        "sender": payload_inner.get("phoneNumber"),
        "text": payload_inner.get("message"),
        "receivedAt": payload_inner.get("receivedAt"),
    }
    canonical = json.dumps(relevant, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest(), canonical


def ots_timestamp(hex_hash: str) -> bytes:
    """Submit hash to OpenTimestamp and return binary .ots proof."""
    payload = {"hash": hex_hash, "algorithm": "sha256"}
    r = requests.post(OTS_ENDPOINT, json=payload, timeout=10)
    r.raise_for_status()
    return r.content


def store_evidence(sms_payload: dict, hex_hash: str, ots_blob: bytes) -> int:
    """Persist evidence to PostgreSQL. Returns evidence_id."""
    if not psycopg2:
        raise RuntimeError("psycopg2-binary required for evidence store")

    conn = psycopg2.connect(DB_DSN)
    cur = conn.cursor()
    payload_inner = sms_payload.get("payload", {})

    insert_sql = """
        INSERT INTO sms_evidence
        (device_id, message_id, sender, text, received_at,
         sha256_hash, ots_proof, created_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,now())
        RETURNING id;
    """
    cur.execute(
        insert_sql,
        (
            sms_payload.get("deviceId"),
            payload_inner.get("messageId"),
            payload_inner.get("phoneNumber"),
            payload_inner.get("message"),
            payload_inner.get("receivedAt"),
            hex_hash,
            psycopg2.Binary(ots_blob) if psycopg2 else ots_blob,
        ),
    )
    evidence_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return evidence_id


def push_openclaw_event(evidence_id: int, sms_payload: dict) -> None:
    """Push minimal event to OpenClaw."""
    headers = {
        "Authorization": f"Bearer {OPENCLAW_TOKEN}",
        "Content-Type": "application/json",
    }
    payload_inner = sms_payload.get("payload", {})
    data = {
        "source": "sms-gate",
        "type": "sms:received",
        "details": {
            "evidence_id": evidence_id,
            "sender": payload_inner.get("phoneNumber"),
            "text": payload_inner.get("message"),
        },
    }
    requests.post(OPENCLAW_URL, json=data, headers=headers, timeout=5).raise_for_status()


@app.route("/openclaw/webhook", methods=["POST"])
def sms_gate_webhook():
    """Handle SMS-Gate webhook with hash, timestamp, store, and forward."""
    if not request.is_json:
        abort(400, "Expected JSON")

    body = request.get_json()

    if "event" not in body or body["event"] != "sms:received":
        abort(400, "Only sms:received events are handled")

    hex_hash, _ = canonical_hash(body)

    try:
        ots_blob = ots_timestamp(hex_hash)
    except Exception as exc:
        print(f"[ERROR] OTS submission failed: {exc}")
        abort(502, "Timestamp service unavailable")

    if DB_DSN and psycopg2:
        try:
            evidence_id = store_evidence(body, hex_hash, ots_blob)
        except Exception as exc:
            print(f"[ERROR] DB insert failed: {exc}")
            abort(502, "Evidence store unavailable")
    else:
        evidence_id = 0

    if OPENCLAW_URL and OPENCLAW_TOKEN:
        try:
            push_openclaw_event(evidence_id, body)
        except Exception as exc:
            print(f"[WARN] Failed to push OpenClaw event: {exc}")

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
