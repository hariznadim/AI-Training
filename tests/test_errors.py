"""
Comprehensive test suite for error handling architecture.

Tests the exception hierarchy, error mapping, and decorator-based
error boundaries.
"""

import pytest

from app.decorators import error_boundary
from app.exceptions import (
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)
from app.mapper import map_exception
from app.models import ErrorResponse


class TestExceptionMapping:
    """Test exception to ErrorResponse mapping."""

    def test_validation_error_maps_to_400(self) -> None:
        """ValidationError should map to HTTP 400 status."""
        exc = ValidationError("Email is invalid")
        response = map_exception(exc)

        assert response.status == 400
        assert response.error_code == "VALIDATION_ERROR"
        assert response.message == "Email is invalid"
        assert response.timestamp is not None

    def test_not_found_error_maps_to_404(self) -> None:
        """NotFoundError should map to HTTP 404 status."""
        exc = NotFoundError("User not found")
        response = map_exception(exc)

        assert response.status == 404
        assert response.error_code == "NOT_FOUND_ERROR"
        assert response.message == "User not found"
        assert response.timestamp is not None

    def test_unauthorized_error_maps_to_401(self) -> None:
        """UnauthorizedError should map to HTTP 401 status."""
        exc = UnauthorizedError("Credentials invalid")
        response = map_exception(exc)

        assert response.status == 401
        assert response.error_code == "UNAUTHORIZED_ERROR"
        assert response.message == "Credentials invalid"
        assert response.timestamp is not None

    def test_unknown_exception_maps_to_500(self) -> None:
        """Unknown exceptions should map to HTTP 500 status."""
        exc = RuntimeError("Something went wrong")
        response = map_exception(exc)

        assert response.status == 500
        assert response.error_code == "INTERNAL_SERVER_ERROR"
        assert response.message == "An unexpected error occurred"
        assert response.timestamp is not None


class TestErrorBoundaryDecorator:
    """Test the error_boundary decorator functionality."""

    def test_decorator_catches_domain_exception(self) -> None:
        """Decorator should catch domain exceptions and return ErrorResponse."""

        @error_boundary
        def failing_operation() -> None:
            raise ValidationError("Invalid input")

        response = failing_operation()

        assert isinstance(response, ErrorResponse)
        assert response.status == 400
        assert response.error_code == "VALIDATION_ERROR"
        assert response.message == "Invalid input"

    def test_decorator_catches_generic_exception(self) -> None:
        """Decorator should catch generic exceptions and return ErrorResponse."""

        @error_boundary
        def failing_operation() -> None:
            raise ValueError("Generic error")

        response = failing_operation()

        assert isinstance(response, ErrorResponse)
        assert response.status == 500
        assert response.error_code == "INTERNAL_SERVER_ERROR"
        # Message should not leak raw exception details
        assert "ValueError" not in response.message
        assert response.message == "An unexpected error occurred"


