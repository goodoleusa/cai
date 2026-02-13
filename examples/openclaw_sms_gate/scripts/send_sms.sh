#!/bin/bash
# -------------------------------------------------
# send_sms.sh - Send a text via SMS-Gate (Linux/macOS)
# -------------------------------------------------
# Arguments:
#   $1 = phone number (E.164, e.g. +11234567890)
#   $2 = message text (quotes required if spaces)
# -------------------------------------------------

if [ -z "$1" ]; then
    echo "Usage: send_sms.sh <phone> <message>"
    exit 1
fi

PHONE="$1"
TEXT="${2:-}"

if [ -z "$SMSGATE_AUTH" ]; then
    echo "Error: SMSGATE_AUTH environment variable not set."
    echo "Set it with base64-encoded credentials: echo -n 'USERNAME:PASSWORD' | base64"
    exit 1
fi

curl -X POST \
     -H "Authorization: Basic $SMSGATE_AUTH" \
     -H "Content-Type: application/json" \
     --data "{\"textMessage\":{\"text\":\"$TEXT\"},\"phoneNumbers\":[\"$PHONE\"]}" \
     https://api.sms-gate.app/3rdparty/v1/messages
