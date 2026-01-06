"""Tests for structured JSON logging and correlation ID injection."""

import json
import logging
from io import StringIO

from security_automation.observability import (
    clear_correlation_id,
    configure_logging,
    get_logger,
    set_correlation_id,
)
from security_automation.observability.context import get_correlation_id


def test_configure_logging_emits_json(capsys):
    """Test that configure_logging sets up JSON output to stdout."""
    # Reset logging
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Configure with defaults
    configure_logging(service_name="test-service", env_name="test")

    logger = get_logger("test_logger")
    logger.info("test_message", extra={"event": "test_event"})

    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")

    # Verify we have at least one line
    assert len(lines) >= 1

    # Parse as JSON
    log_obj = json.loads(lines[-1])

    # Verify required fields
    assert log_obj["level"] == "INFO"
    assert log_obj["message"] == "test_message"
    assert log_obj["service"] == "test-service"
    assert log_obj["env"] == "test"
    assert log_obj["logger"] == "test_logger"
    assert "timestamp" in log_obj
    assert log_obj["timestamp"].endswith("Z")


def test_correlation_id_injected_in_logs(capsys):
    """Test that correlation_id from context is included in every log line."""
    # Reset logging
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Configure logging
    configure_logging()

    # Set a known correlation ID
    test_cid = "test-correlation-id-123"
    set_correlation_id(test_cid)

    logger = get_logger("test_logger")
    logger.info("first log", extra={"event": "event1"})
    logger.info("second log", extra={"event": "event2"})

    captured = capsys.readouterr()
    lines = captured.out.strip().split("\n")

    # Should have at least 2 log lines
    assert len(lines) >= 2

    # Both should have the same correlation_id
    log1 = json.loads(lines[-2])
    log2 = json.loads(lines[-1])

    assert log1["correlation_id"] == test_cid
    assert log2["correlation_id"] == test_cid

    # Cleanup
    clear_correlation_id()


def test_correlation_id_context_isolation():
    """Test that correlation_id context is properly isolated."""
    cid1 = "cid-1"
    set_correlation_id(cid1)
    assert get_correlation_id() == cid1

    cid2 = "cid-2"
    set_correlation_id(cid2)
    assert get_correlation_id() == cid2

    clear_correlation_id()
    assert get_correlation_id() is None
