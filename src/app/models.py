"""
Data models for error responses.

Provides immutable response structures for structured error handling.
"""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class ErrorResponse:
    """Structured error response model.

    Attributes:
        status: HTTP status code.
        error_code: Machine-readable error identifier.
        message: Human-readable error message.
        timestamp: ISO format timestamp when error occurred.
    """

    status: int
    error_code: str
    message: str
    timestamp: str

    @classmethod
    def create(cls, status: int, error_code: str, message: str) -> "ErrorResponse":
        """Create an ErrorResponse with current timestamp.

        Args:
            status: HTTP status code.
            error_code: Machine-readable error identifier.
            message: Human-readable error message.

        Returns:
            ErrorResponse instance with ISO format timestamp.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        return cls(
            status=status,
            error_code=error_code,
            message=message,
            timestamp=timestamp,
        )
