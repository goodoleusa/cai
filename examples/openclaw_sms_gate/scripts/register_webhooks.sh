#!/bin/bash
# Register SMS-Gate webhooks - replace URL with your public HTTPS endpoint
# Requires: curl, base64 or openssl for encoding credentials

WEBHOOK_URL="${1:-https://your-host.example.com/openclaw/webhook}"
USERNAME="${SMSGATE_USER:-}"
PASSWORD="${SMSGATE_PASSWORD:-}"

if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
    echo "Set SMSGATE_USER and SMSGATE_PASSWORD env vars, or pass as args."
    echo "Usage: SMSGATE_USER=user SMSGATE_PASSWORD=pass $0 https://your-host/openclaw/webhook"
    exit 1
fi

AUTH=$(echo -n "$USERNAME:$PASSWORD" | base64 2>/dev/null || echo -n "$USERNAME:$PASSWORD" | openssl base64)

for event in "sms:received" "sms:sent" "sms:delivered"; do
    echo "Registering $event..."
    curl -X POST -u "$USERNAME:$PASSWORD" \
         -H "Content-Type: application/json" \
         -d "{\"event\":\"$event\",\"url\":\"$WEBHOOK_URL\"}" \
         https://api.sms-gate.app/3rdparty/v1/webhooks
    echo ""
done

echo "Done. Verify at https://api.sms-gate.app dashboard."
