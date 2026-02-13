-- SMS evidence store for blockchain timestamping integration
CREATE TABLE IF NOT EXISTS sms_evidence (
    id            SERIAL PRIMARY KEY,
    device_id     TEXT NOT NULL,
    message_id    TEXT NOT NULL,
    sender        TEXT NOT NULL,
    text          TEXT NOT NULL,
    received_at   TIMESTAMPTZ NOT NULL,
    sha256_hash   CHAR(64) NOT NULL,
    ots_proof     BYTEA NOT NULL,
    ipfs_cid      TEXT,
    eth_tx_hash   TEXT,
    created_at    TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_sms_evidence_sha256 ON sms_evidence(sha256_hash);
CREATE INDEX IF NOT EXISTS idx_sms_evidence_sender ON sms_evidence(sender);
CREATE INDEX IF NOT EXISTS idx_sms_evidence_created_at ON sms_evidence(created_at);
