"""
Exception hierarchy for error-architecture.

Provides a structured exception system with error codes and messages
suitable for middleware pipeline processing.
"""


class AppError(Exception):
    """Base exception for application errors.

    Attributes:
        message: Human-readable error message.
        error_code: Machine-readable error identifier.
    """

    def __init__(self, message: str, error_code: str) -> None:
        """Initialize AppError.

        Args:
            message: The error message.
            error_code: The error code identifier.
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationError(AppError):
    """Raised when input validation fails."""

    def __init__(self, message: str) -> None:
        """Initialize ValidationError.

        Args:
            message: The validation error message.
        """
        super().__init__(message, "VALIDATION_ERROR")


class NotFoundError(AppError):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str) -> None:
        """Initialize NotFoundError.

        Args:
            message: The not found error message.
        """
        super().__init__(message, "NOT_FOUND_ERROR")


class UnauthorizedError(AppError):
    """Raised when a user is not authorized to perform an action."""

    def __init__(self, message: str) -> None:
        """Initialize UnauthorizedError.

        Args:
            message: The authentication/authorization error message.
        """
        super().__init__(message, "UNAUTHORIZED_ERROR")
