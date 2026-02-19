"""
error-architecture: Production-grade error handling with middleware pipelines.

A structured exception handling framework inspired by C# middleware pipelines,
providing:
- Exception hierarchy with error codes
- Structured error responses
- Centralized error mapping
- Decorator-based error boundaries
- Integrated logging
"""

from app.decorators import error_boundary
from app.exceptions import AppError, NotFoundError, UnauthorizedError, ValidationError
from app.mapper import map_exception
from app.models import ErrorResponse

__version__ = "0.1.0"
__all__ = [
    "AppError",
    "ValidationError",
    "NotFoundError",
    "UnauthorizedError",
    "ErrorResponse",
    "error_boundary",
    "map_exception",
]
