"""Correlation ID context using contextvars for async-safe propagation."""

from contextvars import ContextVar
from typing import Optional

_correlation_id_var: ContextVar[Optional[str]] = ContextVar(
    "correlation_id", default=None
)


def set_correlation_id(value: str) -> None:
    """
    Set the correlation ID for the current context.

    Args:
        value: Unique identifier for correlating logs across the execution.
    """
    _correlation_id_var.set(value)


def get_correlation_id() -> Optional[str]:
    """
    Get the current correlation ID from context.

    Returns:
        The correlation ID or None if not set.
    """
    return _correlation_id_var.get()


def clear_correlation_id() -> None:
    """Clear the correlation ID from context."""
    _correlation_id_var.set(None)
