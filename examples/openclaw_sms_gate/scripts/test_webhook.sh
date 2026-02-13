#!/bin/bash
# Test script for webhook endpoint - simulates an incoming SMS payload

WEBHOOK_URL="${1:-http://localhost:5000/openclaw/webhook}"

cat <<EOF | curl -s -X POST -H "Content-Type: application/json" -d @- "$WEBHOOK_URL"
{
  "deviceId":"ffffffffceb0b1db0000018e937c815b",
  "event":"sms:received",
  "id":"Ey6ECgOkVVFjz3CL48B8C",
  "payload":{
    "messageId":"abc123",
    "message":"Test from OpenClaw webhook",
    "phoneNumber":"+15551234567",
    "simNumber":1,
    "receivedAt":"2024-09-01T12:34:56.000+00:00"
  },
  "webhookId":"LreFUt-Z3sSq0JufY9uWB"
}
EOF
echo ""
