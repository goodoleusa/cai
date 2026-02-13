"""
SMS-Gate send_sms tool for CAI/OpenClaw agents.

Sends SMS messages via SMS-Gate (Graphene Android). Requires SMSGATE_AUTH
environment variable with base64-encoded credentials (username:password).
"""

import os

from cai.sdk.agents import function_tool

SMS_GATE_API_URL = "https://api.sms-gate.app/3rdparty/v1/messages"


@function_tool
def send_sms(phone: str, message: str) -> str:
    """
    Send an SMS message via SMS-Gate (Graphene Android number).

    Use this tool when the user or workflow requires sending a text message
    to a phone number. Ideal for security alerts, OTP delivery, or notifications.

    Args:
        phone: Destination phone number in E.164 format (e.g. +11234567890).
        message: The text message to send.

    Returns:
        str: API response status (e.g., "queued", "sent") or error message.
    """
    auth = os.getenv("SMSGATE_AUTH")
    if not auth:
        return "Error: SMSGATE_AUTH environment variable not set. Set it with base64-encoded credentials."

    import requests

    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
    }
    payload = {
        "textMessage": {"text": message},
        "phoneNumbers": [phone],
    }

    try:
        response = requests.post(
            SMS_GATE_API_URL,
            json=payload,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        status = data.get("status", "unknown")
        msg_id = data.get("id", "")
        return f"SMS queued successfully. Status: {status}, ID: {msg_id}"
    except requests.RequestException as e:
        return f"Failed to send SMS: {str(e)}"
