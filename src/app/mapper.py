"""
Centralized error mapping for exception handling.

Maps exceptions to structured error responses for consistent error handling
across the application.
"""

import logging
from typing import Any

from app.exceptions import AppError, NotFoundError, UnauthorizedError, ValidationError
from app.models import ErrorResponse

logger = logging.getLogger(__name__)


def map_exception(exc: Exception) -> ErrorResponse:
    """Map an exception to a structured error response.

    Handles both domain exceptions (AppError subclasses) and unexpected
    exceptions. Logs full stack trace for all errors without re-raising.

    Args:
        exc: The exception to map.

    Returns:
        An ErrorResponse with appropriate status code and message.
    """
    # First, log the full exception with stack trace
    logger.error("Exception occurred:", exc_info=True)

    # Map custom domain exceptions
    if isinstance(exc, ValidationError):
        return ErrorResponse.create(
            status=400,
            error_code=exc.error_code,
            message=exc.message,
        )

    if isinstance(exc, NotFoundError):
        return ErrorResponse.create(
            status=404,
            error_code=exc.error_code,
            message=exc.message,
        )

    if isinstance(exc, UnauthorizedError):
        return ErrorResponse.create(
            status=401,
            error_code=exc.error_code,
            message=exc.message,
        )

    # Map other AppError subclasses
    if isinstance(exc, AppError):
        return ErrorResponse.create(
            status=500,
            error_code=exc.error_code,
            message=exc.message,
        )

    # Map unknown exceptions
    return ErrorResponse.create(
        status=500,
        error_code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred",
    )
