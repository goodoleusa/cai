"""
SMS-Gate webhook receiver for OpenClaw/CAI integration.

Receives inbound SMS events from SMS-Gate and forwards them to OpenClaw's
event API. Deploy this behind a reverse proxy (nginx, Caddy) with HTTPS.

Set env vars: OPENCLAW_URL, OPENCLAW_TOKEN
"""

import os

import requests
from flask import Flask, abort, request

app = Flask(__name__)

OPENCLAW_URL = os.getenv("OPENCLAW_URL")  # e.g. https://oc.mycorp.com/api/v1/events
OPENCLAW_TOKEN = os.getenv("OPENCLAW_TOKEN")


def forward_to_openclaw(event_name: str, payload: dict) -> None:
    """Forward SMS-Gate event to OpenClaw REST API."""
    headers = {
        "Authorization": f"Bearer {OPENCLAW_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "source": "sms-gate",
        "type": event_name,
        "timestamp": payload.get("receivedAt") or payload.get("sentAt"),
        "details": {
            "device_id": payload.get("deviceId"),
            "message_id": payload.get("payload", {}).get("messageId"),
            "sender": payload.get("payload", {}).get("phoneNumber"),
            "text": payload.get("payload", {}).get("message"),
        },
    }
    resp = requests.post(OPENCLAW_URL, json=data, headers=headers, timeout=5)
    resp.raise_for_status()


@app.route("/openclaw/webhook", methods=["POST"])
def sms_gate_webhook():
    """Handle SMS-Gate webhook POST."""
    if not request.is_json:
        abort(400, "Expected JSON")

    body = request.get_json()

    if "event" not in body or "payload" not in body:
        abort(400, "Missing required fields")

    try:
        forward_to_openclaw(body["event"], body)
    except Exception as e:
        print(f"Error forwarding to OpenClaw: {e}")

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
