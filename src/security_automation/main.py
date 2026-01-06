import os
import sys
import uuid
from typing import Optional

from security_automation.observability import (
    clear_correlation_id,
    configure_logging,
    get_logger,
    set_correlation_id,
)

logger = get_logger(__name__)


def get_correlation_id_from_env() -> Optional[str]:
    """
    Retrieve correlation ID from environment variable or None.

    Returns:
        Correlation ID if set, None otherwise.
    """
    return os.getenv("CORRELATION_ID")


def main(correlation_id: Optional[str] = None) -> None:
    """
    Main entrypoint for security automation CLI with observability.

    Args:
        correlation_id: Optional correlation ID (for testing/chaining).
    """
    # Initialize logging
    configure_logging()

    # Set correlation ID: from arg, env var, or generate new one
    cid = correlation_id or get_correlation_id_from_env() or str(uuid.uuid4())
    set_correlation_id(cid)

    try:
        logger.info("run_started", extra={"event": "run_started"})

        logger.info("initializing security automation tasks", extra={"event": "init_tasks"})

        # Simulate policy evaluation
        logger.info("evaluating security policies", extra={"event": "policy_evaluated"})

        # Simulate automation execution
        logger.info("executing automated remediation", extra={"event": "automation_executed"})

        logger.info("security automation completed successfully", extra={"event": "run_completed"})

    except Exception as e:
        logger.exception("security automation failed", extra={"event": "run_failed"}, exc_info=True)
        sys.exit(1)
    finally:
        clear_correlation_id()


if __name__ == "__main__":
    main()
