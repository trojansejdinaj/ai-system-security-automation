
Source: :contentReference[oaicite:0]{index=0}

---

## Updated `docs/decisions/0003-logging-and-correlation-ids.md`

Key changes:
- Adds an explicit note about `src/` layout + `PYTHONPATH` / editable install.
- Tightens lifecycle statement to match your implementation (and your log proof).
- Keeps everything else intact.

```md
# ADR 0003: Logging and Correlation IDs

**Status:** Accepted  
**Date:** 2026-01-06

## Title

Implement structured JSON logging with automatic correlation ID injection using ContextVar

## Context

As the security automation system evolves from a proof-of-concept to a production-like system, we need observability capabilities to:

- Trace execution flows across multiple function calls
- Correlate logs from a single run for debugging and auditing
- Support future centralized logging and monitoring
- Enable operators to investigate security incidents with full context

Previous approach: ad-hoc print() statements, no structure, no correlation.

Current challenges:
- Impossible to correlate logs from a single execution
- No machine-readable format for log aggregation
- No standard event naming for semantic querying
- No environment awareness (dev vs. prod)

## Decision

Implement structured JSON logging with automatic correlation ID injection:

1. **JSON Logging**: All logs emit as single-line JSON objects to stdout
   - Machine-readable and easily parsed by log aggregation tools
   - Standard schema with required fields: timestamp, level, service, env, correlation_id, event, message, logger, module
   - Optional fields for exceptions and custom attributes

2. **Correlation IDs via ContextVar**: Use Python's `contextvars.ContextVar` for correlation ID storage
   - Async-safe and thread-safe (no global mutable state)
   - Automatically injected into every log record
   - Lifecycle: generated (or provided) at process start, persists across execution, cleared on exit
   - Users can override via `CORRELATION_ID` environment variable

3. **Configuration via Environment Variables**:
   - `LOG_LEVEL`: Control verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL)
   - `ENV`: Identify deployment environment (local, dev, staging, prod)
   - `SERVICE_NAME`: Service identifier (for multi-service setups)
   - `CORRELATION_ID`: Optional override for correlation ID

4. **stdlib logging**: Use Python's built-in logging module
   - No heavy external dependencies
   - Familiar to Python developers
   - Custom formatter for JSON output and correlation ID injection

5. **Semantic Events**: Include an `event` field for high-level operation names
   - Examples: `run_started`, `policy_evaluated`, `automation_executed`, `run_failed`
   - Enables grep/filtering for specific phases of execution

## Consequences

### Positive

- **Full traceability**: All logs from a single run can be traced via correlation_id
- **Machine-readable**: JSON format integrates with log aggregation platforms (DataDog, Splunk, Cloud Logging, etc.)
- **Async-safe**: ContextVar ensures correlation IDs don't leak between concurrent tasks
- **Low overhead**: stdlib logging + standard Python libraries only
- **Environment-aware**: Easy to distinguish local vs. production logs
- **Semantic queries**: Event names enable filtering and timeline analysis
- **Future-proof**: Foundation for distributed tracing, metrics, and alerting

### Negative

- **Verbosity**: JSON output is more voluminous than simple text logs (mitigated by careful field selection)
- **Readability**: Raw JSON is less human-friendly without tools like `jq` (minor issue for automated systems)
- **Debugging overhead**: Must configure logging and set correlation IDs in all entrypoints
- **Compat**: If switching to a different logging library later, formatters must be rewritten

### Neutral

- **No dependency lock-in**: Can replace implementation without changing calling code (set_correlation_id, get_logger remain stable)
- **Performance**: Minimal impact (JSON serialization overhead is negligible for typical log volumes)

## Alternatives Considered

### 1. Text-based structured logs (key=value format)
- Simpler to parse with regex
- Rejected: JSON is more standard and better for nested data

### 2. Global variables for correlation ID
- Simpler initial implementation
- Rejected: Not thread-safe or async-safe; would break in concurrent scenarios

### 3. Pass correlation ID as argument to every function
- Explicit and traceable
- Rejected: High boilerplate, invasive to codebase; ContextVar is cleaner

### 4. Use a heavyweight logging framework (structlog, python-json-logger)
- More features out-of-the-box
- Rejected: stdlib logging is sufficient; minimal dependencies preferred

### 5. Emit logs to a file instead of stdout
- Decouples logging from container orchestration
- Rejected: Stdout is simpler for containerized deployments; container orchestration handles rotation

### 6. Automatic correlation ID from HTTP headers (for future API)
- Enables tracing across services
- Deferred: Not applicable to current CLI app; can be added when CLI becomes a service

## Implementation

- **Modules**:
  - `observability/context.py`: ContextVar wrapper (set_correlation_id, get_correlation_id, clear_correlation_id)
  - `observability/logging.py`: JSONFormatter and configure_logging() helper
  - `observability/__init__.py`: Public API

- **Integration**:
  - `main.py`: Initialize logging at startup, generate/read correlation ID, set in context
  - `Makefile`: Add `run` and `demo-log` targets

- **Testing**:
  - Verify JSON output structure
  - Verify correlation ID is injected
  - Verify isolation between contexts

### Note on `src/` layout execution
This repository uses a `src/` layout. Until the package is installed in editable mode (recommended), module execution may require `PYTHONPATH=src` for `python -m security_automation` to resolve correctly. The Makefile can set this for local development, or you can run `uv pip install -e .` to avoid relying on `PYTHONPATH`.

## Acceptance Criteria

- ✅ All logs emitted as valid JSON
- ✅ Correlation ID present on every log line
- ✅ Correlation ID can be set via CORRELATION_ID env var
- ✅ LOG_LEVEL, ENV, SERVICE_NAME configurable via env vars
- ✅ `make run` / `make demo-log` produces logs with same correlation_id across all events
- ✅ Architecture doc explains correlation ID lifecycle and querying
- ✅ Tests verify JSON schema and correlation ID injection

## Related ADRs

- ADR-0001: Repo Standards (code structure, testing, CI/CD)
- ADR-0002: Secrets Model and Rotation (handling sensitive data in logs—ensure no secrets are logged)
