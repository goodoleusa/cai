"""
CAI agent with SMS-Gate integration.

This example shows how to use the send_sms tool with a CAI agent for
security alerts and notifications. Set SMSGATE_AUTH before running.

Usage:
  export SMSGATE_AUTH=$(echo -n 'USER:PASS' | base64)
  python -m examples.openclaw_sms_gate.main
"""

import asyncio
import os

from cai.sdk.agents import Agent, Runner, trace
from cai.sdk.agents.models import OpenAIChatCompletionsModel

from examples.openclaw_sms_gate.send_sms_tool import send_sms  # noqa: E402


async def main():
    if not os.getenv("SMSGATE_AUTH"):
        print(
            "Set SMSGATE_AUTH first: export SMSGATE_AUTH=$(echo -n 'USER:PASS' | base64)"
        )
        return

    agent = Agent(
        name="SMS Alert Agent",
        instructions="""You are a security operations assistant with SMS notification capabilities.
When the user asks to send an alert or notification via SMS, use the send_sms tool.
Always confirm phone numbers are in E.164 format (+country_code + number) before sending.
Keep messages brief and actionable for security alerts.""",
        model=OpenAIChatCompletionsModel(model="gpt-4o-mini"),
        tools=[send_sms],
    )

    with trace("SMS Gate example"):
        result = await Runner.run(
            agent,
            "Send a test SMS to +15551234567 saying 'CAI SMS-Gate test alert'",
        )
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
