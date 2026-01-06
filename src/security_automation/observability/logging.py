"""Structured JSON logging configuration with correlation ID injection."""

import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any, Optional

from security_automation.observability.context import get_correlation_id


class JSONFormatter(logging.Formatter):
    """Custom formatter that emits JSON-structured logs with correlation ID injection."""

    def __init__(self, service_name: str = "ai-system-security-automation", env: str = "local"):
        """
        Initialize the JSON formatter.

        Args:
            service_name: Service identifier for logs.
            env: Environment name (local, dev, prod, etc.).
        """
        super().__init__()
        self.service_name = service_name
        self.env = env

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record as a single-line JSON object.

        Args:
            record: The log record to format.

        Returns:
            A JSON string with all required fields.
        """
        # Prepare base fields
        log_dict: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "level": record.levelname,
            "service": self.service_name,
            "env": self.env,
            "correlation_id": get_correlation_id(),
            "event": record.getMessage() if hasattr(record, "event") else None,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
        }

        # Handle exceptions
        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            log_dict["exception"] = record.exc_text

        # Add any extra fields from the LogRecord
        for key, value in record.__dict__.items():
            if key not in {
                "name",
                "msg",
                "args",
                "created",
                "taskName",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "module",
                "msecs",
                "message",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "thread",
                "threadName",
                "exc_info",
                "exc_text",
                "stack_info",
                "getMessage",
            }:
                log_dict[key] = value

        # Emit as single-line JSON
        return json.dumps(log_dict, default=str)


def configure_logging(
    service_name: Optional[str] = None, env_name: Optional[str] = None
) -> None:
    """
    Configure stdlib logging to emit structured JSON logs to stdout.

    Args:
        service_name: Service name (defaults to env var SERVICE_NAME or default).
        env_name: Environment name (defaults to env var ENV or "local").
    """
    service_name = service_name or os.getenv("SERVICE_NAME", "ai-system-security-automation")
    env_name = env_name or os.getenv("ENV", "local")
    log_level = os.getenv("LOG_LEVEL", "INFO")

    # Get root logger
    root_logger = logging.getLogger()

    # Clear any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Set level
    root_logger.setLevel(log_level.upper())

    # Create stdout handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level.upper())

    # Attach JSON formatter
    formatter = JSONFormatter(service_name=service_name, env=env_name)
    handler.setFormatter(formatter)

    # Add handler to root logger
    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (typically __name__).

    Returns:
        A configured logger instance.
    """
    return logging.getLogger(name)
