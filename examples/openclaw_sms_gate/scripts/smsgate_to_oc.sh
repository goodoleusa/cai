#!/bin/bash
# smsgate_to_oc.sh - Pipe SMS-Gate webhook JSON to OpenClaw CLI
# Configure your web server (nginx, Apache, Caddy) to pipe the request body to this script.

read -r payload

event=$(echo "$payload" | jq -r '.event')
msg=$(echo "$payload" | jq -r '.payload.message')
sender=$(echo "$payload" | jq -r '.payload.phoneNumber')
msgid=$(echo "$payload" | jq -r '.payload.messageId')

cat <<EOF | openclaw event push -
{
  "source": "sms-gate",
  "type": "$event",
  "details": {
    "sender": "$sender",
    "text": "$msg",
    "message_id": "$msgid"
  }
}
EOF
