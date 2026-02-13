# OpenClaw SMS-Gate Integration

Integrate SMS-Gate (Graphene Android) with CAI/OpenClaw for outbound SMS alerts and inbound webhook events. Includes optional blockchain timestamping for evidence preservation.

## Quick Start

### 1. Set Up Credentials

**Linux/macOS:**
```bash
export SMSGATE_AUTH=$(echo -n 'USERNAME:PASSWORD' | base64)
```

**Windows (PowerShell):**
```powershell
$cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("USERNAME:PASSWORD"))
[Environment]::SetEnvironmentVariable("SMSGATE_AUTH", $cred, "User")
```

### 2. Send SMS via CAI Agent

```bash
export SMSGATE_AUTH=$(echo -n 'USER:PASS' | base64)
python -m examples.openclaw_sms_gate.main
```

Or use the `send_sms` tool in your own agent:

```python
from examples.openclaw_sms_gate.send_sms_tool import send_sms
from cai.sdk.agents import Agent

agent = Agent(
    name="Alert Agent",
    tools=[send_sms],
    ...
)
```

### 3. Send SMS via Scripts

**Bash (Linux/macOS):**
```bash
chmod +x examples/openclaw_sms_gate/scripts/send_sms.sh
./examples/openclaw_sms_gate/scripts/send_sms.sh +11234567890 "Test message"
```

**Windows Batch:** `send_sms.bat +11234567890 "Test message"`  
**PowerShell:** `Send-Sms.ps1 -Phone "+11234567890" -Message "Test message"`

---

## Inbound SMS (Webhooks)

### Basic Webhook Receiver

Receives SMS-Gate events and forwards to OpenClaw:

```bash
export OPENCLAW_URL=https://your-openclaw.example.com/api/v1/events
export OPENCLAW_TOKEN=your-bearer-token
python -m examples.openclaw_sms_gate.webhook_receiver
```

### Blockchain Webhook (OpenTimestamp + Evidence Store)

Computes SHA-256, submits to OpenTimestamp, stores in PostgreSQL:

```bash
export OPENCLAW_URL=...
export OPENCLAW_TOKEN=...
export DATABASE_URL=postgresql://user:pass@localhost/sms_evidence
pip install psycopg2-binary
createdb sms_evidence && psql -f examples/openclaw_sms_gate/database/schema.sql
python -m examples.openclaw_sms_gate.webhook_receiver_blockchain
```

### Register Webhooks with SMS-Gate

```bash
SMSGATE_USER=user SMSGATE_PASSWORD=pass \
  ./scripts/register_webhooks.sh https://your-host.example.com/openclaw/webhook
```

### Test Webhook

```bash
./scripts/test_webhook.sh http://localhost:5000/openclaw/webhook
```

---

## OpenClaw Config

Add to your OpenClaw `config.yaml`:

```yaml
notifications:
  sms_gate:
    command: "send_sms.sh {phone} \"{message}\""

rules:
  - name: "New IOC detected"
    condition: "ioc.type == 'malicious_url'"
    actions:
      - notify:
          method: sms_gate
          phone: "+1123446789"
          message: "⚠️ New malicious URL: {ioc.value}"
```

See `config/openclaw_config_example.yaml` for full examples.

---

## Files

| File | Purpose |
|------|---------|
| `send_sms_tool.py` | CAI `function_tool` for agents |
| `webhook_receiver.py` | Flask app: SMS-Gate → OpenClaw |
| `webhook_receiver_blockchain.py` | + OpenTimestamp + PostgreSQL |
| `scripts/send_sms.sh` | Bash send script |
| `scripts/send_sms.bat` | Windows batch script |
| `scripts/Send-Sms.ps1` | PowerShell script |
| `scripts/smsgate_to_oc.sh` | CLI bridge (jq + openclaw) |
| `scripts/register_webhooks.sh` | Register webhooks with SMS-Gate |
| `scripts/test_webhook.sh` | Test webhook endpoint |
| `database/schema.sql` | PostgreSQL evidence table |

---

## Security Notes

- **Never hardcode credentials.** Use `SMSGATE_AUTH` env var or a secrets manager.
- Use HTTPS for webhook endpoints in production.
- Encrypt sensitive columns (e.g., `text`) at rest for compliance.
- Follow retention policies for personal data (GDPR/CCPA).

---

## Verification (Blockchain)

To verify stored proofs later:

```bash
pip install opentimestamps-client
ots verify --hash <hex_hash> --file proof.ots
```
