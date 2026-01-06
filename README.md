# ai-system-security-automation

Umbrella security automation portfolio for the Applied AI Systems stack.
This repo hosts the shared lab baseline + standards + reusable security automation patterns.

## Sub-portfolios (specializations)
- Identity & Access Automation
- Cloud Security Posture Automation (CSPM)
- Threat Detection Automation
## Observability & Logging

This system emits **structured JSON logs** with automatic **correlation IDs** for tracing execution across the entire process.

### How It Works

- Every run generates a unique correlation ID (UUID) automatically
- All logs from that run share the same correlation ID
- Logs are emitted as single-line JSON to stdout for easy parsing and aggregation
- You can provide your own correlation ID via the `CORRELATION_ID` environment variable

### Example Log Output

```json
{"timestamp":"2026-01-06T15:30:45.123456Z","level":"INFO","service":"ai-system-security-automation","env":"local","correlation_id":"a7f2c4d1-8e9b-4c2a-9f3b-1e2d3c4f5a6b","event":"run_started","message":"run_started","logger":"security_automation.main","module":"main"}
{"timestamp":"2026-01-06T15:30:45.234567Z","level":"INFO","service":"ai-system-security-automation","env":"local","correlation_id":"a7f2c4d1-8e9b-4c2a-9f3b-1e2d3c4f5a6b","event":"policy_evaluated","message":"evaluating security policies","logger":"security_automation.main","module":"main"}
{"timestamp":"2026-01-06T15:30:45.345678Z","level":"INFO","service":"ai-system-security-automation","env":"local","correlation_id":"a7f2c4d1-8e9b-4c2a-9f3b-1e2d3c4f5a6b","event":"run_completed","message":"security automation completed successfully","logger":"security_automation.main","module":"main"}
```

### Running the Application

```bash
# Basic run (generates new correlation ID)
make run

# Run with custom correlation ID
CORRELATION_ID=my-trace-id make run

# View logging documentation
see docs/architecture/logging.md
```
## Quickstart
This repo is intentionally lightweight. Each week’s lab lives under `labs/`.
Start with: `labs/week-01` (repo standards + lab scaffold).

## Structure
- `labs/` weekly lab writeups + artifacts
- `docs/` architecture, standards, patterns
- `ops/` runbooks, checklists, hardening notes
- `scripts/` helper scripts
