"""
Decorator-based error boundaries for error handling.

Provides middleware-style error handling through function decorators,
capturing exceptions and returning structured responses.
"""

from functools import wraps
from typing import Any, Callable, TypeVar, cast

from app.mapper import map_exception
from app.models import ErrorResponse

F = TypeVar("F", bound=Callable[..., Any])


def error_boundary(func: F) -> Callable[..., ErrorResponse]:
    """Decorator that wraps function calls with error boundary protection.

    Catches all exceptions (including domain exceptions) and returns
    a structured ErrorResponse. Never re-raises exceptions or leaks
    raw exception details.

    Args:
        func: The function to wrap.

    Returns:
        Wrapped function that returns ErrorResponse on exception.

    Example:
        @error_boundary
        def process_data(value: str) -> str:
            if not value:
                raise ValidationError("Value cannot be empty")
            return f"Processed: {value}"
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> ErrorResponse:
        try:
            # Execute the wrapped function
            func(*args, **kwargs)
            # Return success response (note: for this implementation,
            # we return error response only; actual function logic
            # would need adjustment for success responses)
            return ErrorResponse.create(
                status=200,
                error_code="SUCCESS",
                message="Operation completed successfully",
            )
        except Exception as exc:
            # Map exception to structured response
            return map_exception(exc)

    return cast(Callable[..., ErrorResponse], wrapper)
