# SMS-Gate Integration (OpenClaw)

Integrate [SMS-Gate](https://sms-gate.app) (Graphene Android) with CAI for outbound SMS alerts and inbound webhook events. Optional blockchain timestamping for evidence preservation.

## Overview

| Feature | Description |
|---------|-------------|
| **Outbound SMS** | CAI agents send alerts via `send_sms` tool or shell scripts |
| **Inbound Webhooks** | SMS-Gate POSTs events to your server → forward to OpenClaw/CAI |
| **Blockchain** | OpenTimestamp + PostgreSQL for tamper-evident evidence |

## Quick Start

### 1. Credentials

```bash
export SMSGATE_AUTH=$(echo -n 'USERNAME:PASSWORD' | base64)
```

### 2. Use in CAI Agent

```python
from examples.openclaw_sms_gate.send_sms_tool import send_sms
from cai.sdk.agents import Agent

agent = Agent(
    name="Security Alert Agent",
    tools=[send_sms],
    ...
)
```

### 3. Run Example

```bash
python -m examples.openclaw_sms_gate.main
```

## Full Documentation

See [examples/openclaw_sms_gate/README.md](../../examples/openclaw_sms_gate/README.md) for:

- Shell scripts (bash, batch, PowerShell)
- Webhook receivers (basic + blockchain)
- OpenClaw config examples
- Database schema
- Security considerations
