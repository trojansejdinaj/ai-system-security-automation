# Logging Architecture

## Overview

The AI System Security Automation system uses **structured JSON logging** with **correlation IDs** to provide complete observability of execution flows. All logs are emitted to stdout as single-line JSON objects, enabling easy parsing, aggregation, and tracing.

## Log Schema

Every log line is a valid JSON object with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `timestamp` | ISO-8601 UTC string | When the log was emitted (ends with `Z`) |
| `level` | string | Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `service` | string | Service identifier (default: `ai-system-security-automation`) |
| `env` | string | Environment name (local, dev, staging, prod) |
| `correlation_id` | string or null | Unique ID linking all logs for a single execution |
| `event` | string or null | Semantic event name (e.g., `run_started`, `policy_evaluated`) |
| `message` | string | Log message text |
| `logger` | string | Logger name (typically module path, e.g., `security_automation.main`) |
| `module` | string | Module name where log was emitted |
| `exception` | string (optional) | Full exception traceback if exc_info=True |

## Correlation ID Lifecycle

For a CLI application like this:

1. **Generation**: At process startup, the system either:
   - Uses the `CORRELATION_ID` environment variable if set
   - Generates a new UUID (v4) if not set
   
2. **Storage**: The correlation ID is stored in a `ContextVar` (`correlation_id_var`), which:
   - Is async-safe (won't leak between concurrent tasks)
   - Persists for the entire execution context
   - Is cleared at process shutdown (optional)

3. **Injection**: Every log record automatically includes the current correlation ID via:
   - Custom `JSONFormatter` that calls `get_correlation_id()` for each record
   - No manual setup required; injection is transparent

4. **Cleanup**: Context is cleared after execution completes (optional but good practice)

## How to Trace Execution

### By Correlation ID

All logs for a single run share the same `correlation_id`. To find all logs for a run:

```bash
# Set correlation ID and run
CORRELATION_ID=trace-123 make run | tee logs.jsonl

# Later, find all logs for that trace
grep trace-123 logs.jsonl | jq .

# Count events in a trace
grep trace-123 logs.jsonl | jq -r .event | sort | uniq -c
```

### By Event Type

Logs include semantic event names for easier filtering:

```bash
# Find all policy evaluations
grep '"event":"policy_evaluated"' logs.jsonl | jq .

# Timeline of all events
jq -r '"\(.timestamp) \(.event)"' logs.jsonl
```

## Configuration

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CORRELATION_ID` | (generate UUID) | Override auto-generated correlation ID |
| `LOG_LEVEL` | `INFO` | Minimum log level to emit (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `ENV` | `local` | Environment name for logs |
| `SERVICE_NAME` | `ai-system-security-automation` | Service identifier |

Example:

```bash
# Run with custom correlation ID and debug logging
CORRELATION_ID=my-trace LOG_LEVEL=DEBUG ENV=staging make run
```

## Implementation Details

### Modules

- **`observability/context.py`**: ContextVar management for correlation ID
  - `set_correlation_id(value)`: Set correlation ID
  - `get_correlation_id()`: Retrieve correlation ID
  - `clear_correlation_id()`: Clear correlation ID

- **`observability/logging.py`**: Logging configuration and JSON formatting
  - `JSONFormatter`: Custom formatter emitting single-line JSON
  - `configure_logging()`: Initialize logging with JSON output to stdout
  - `get_logger()`: Retrieve a logger instance

- **`main.py`**: CLI entrypoint wiring logging and setting correlation ID

### Design Rationale

1. **ContextVar over globals**: Async-safe, thread-safe, no global mutable state
2. **JSON over text**: Machine-readable, easy to parse and aggregate
3. **Stdout only**: Simplifies deployment, logging collection via container orchestration
4. **No extra dependencies**: Uses Python stdlib (logging, json, contextvars)

## Example Log Flow

```
Process starts
  ↓
Generate/read CORRELATION_ID: "abc-123"
  ↓
set_correlation_id("abc-123")
  ↓
emit: event="run_started", correlation_id="abc-123"
  ↓
evaluate policies
  ↓
emit: event="policy_evaluated", correlation_id="abc-123"
  ↓
execute automation
  ↓
emit: event="automation_executed", correlation_id="abc-123"
  ↓
emit: event="run_completed", correlation_id="abc-123"
  ↓
clear_correlation_id()
  ↓
Exit
```

## Querying Logs

### Pretty-print logs:
```bash
make run | jq .
```

### Filter by correlation ID:
```bash
make run | jq 'select(.correlation_id == "abc-123")'
```

### Count events by type:
```bash
make run | jq -r .event | sort | uniq -c
```

### Extract timeline:
```bash
make run | jq -r '[.timestamp, .event, .message] | @csv'
```

## Future Extensions

- Add request-scoped context (IP, user, etc.)
- Integrate with cloud logging (Cloud Logging, DataDog, etc.)
- Add sampling/filtering for high-volume scenarios
- Support structured fields beyond standard schema
