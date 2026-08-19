"""Time utility module."""

from datetime import UTC, datetime

def utcnow() -> datetime:
    """Get current time in UTC."""
    return datetime.now(UTC)
