# error-architecture

A production-grade Python error handling framework inspired by C# middleware pipelines. Provides structured exception handling, centralized error mapping, and decorator-based error boundaries for robust application error management.

## Architecture Overview

The error-architecture framework implements a sophisticated error handling system with the following key components:

### 1. **Exception Hierarchy**
- `AppError`: Base exception with `message` and `error_code` attributes
  - `ValidationError`: Input validation failures (HTTP 400)
  - `NotFoundError`: Resource not found (HTTP 404)
  - `UnauthorizedError`: Authorization failures (HTTP 401)

### 2. **Structured Error Response**
Immutable `ErrorResponse` dataclass with:
- `status`: HTTP status code
- `error_code`: Machine-readable error identifier
- `message`: Human-readable error description
- `timestamp`: ISO format timestamp of error occurrence

### 3. **Centralized Error Mapper**
`map_exception(exc: Exception) -> ErrorResponse`
- Maps all exception types to structured responses
- Logs full stack traces without re-raising
- Never leaks raw exception details
- Handles domain and unknown exceptions

### 4. **Decorator-Based Error Boundaries**
`@error_boundary` decorator
- Wraps functions with exception handling
- Returns `ErrorResponse` on any exception
- Fully typed and mypy --strict compatible
- Prevents exception propagation up the call stack

### 5. **Logging Integration**
- ERROR level logging with full stack traces
- Professional formatting with timestamps
- Exception context captured for debugging

## Installation

Clone the repository and install with Poetry:

```bash
cd error-architecture
poetry install
```

## Usage

### CLI Example

Run the CLI example demonstrating validation error handling:

```bash
poetry run python -m app.cli
```

**Expected Output:**
```
Example 1: Valid username
  Status: 200
  Message: Operation completed successfully
  Timestamp: 2026-02-19T15:30:45.123456+00:00

Example 2: Invalid username (too short)
  Status: 400
  Error Code: VALIDATION_ERROR
  Message: Username must be at least 3 characters long
  Timestamp: 2026-02-19T15:30:45.234567+00:00

Example 3: Empty username
  Status: 400
  Error Code: VALIDATION_ERROR
  Message: Username cannot be empty
  Timestamp: 2026-02-19T15:30:45.345678+00:00
```

### API Example

Run the API example demonstrating NotFoundError handling:

```bash
poetry run python -m app.api_example
```

**Expected Output:**
```
API Example: Fetching users

Request: GET /users/1
  Status: 200
  Message: User retrieved: Alice

Request: GET /users/999
  Status: 404
  Error Code: NOT_FOUND_ERROR
  Message: User with ID 999 not found
```

### Using in Your Code

```python
from app import error_boundary, ValidationError, NotFoundError

@error_boundary
def process_user_data(user_id: int, email: str) -> str:
    """Process user data with error handling."""
    if not email:
        raise ValidationError("Email cannot be empty")
    
    if user_id < 0:
        raise NotFoundError(f"User {user_id} not found")
    
    return f"Processing user {user_id}"

# Call the decorated function
response = process_user_data(-1, "test@example.com")
# Returns: ErrorResponse(status=404, error_code="NOT_FOUND_ERROR", ...)
```

## Testing

Run the comprehensive test suite with pytest:

```bash
poetry run pytest -v
```

Tests verify:
- ✓ ValidationError maps to 400
- ✓ NotFoundError maps to 404
- ✓ UnauthorizedError maps to 401
- ✓ Unknown exceptions map to 500
- ✓ Decorator catches domain exceptions
- ✓ Decorator catches generic exceptions

All tests should pass with 100% coverage of error handling paths.

## Type Checking

Verify strict type compliance with mypy:

```bash
poetry run mypy
```

The project is configured with `mypy --strict` mode:
- All functions have return types
- All parameters are typed
- No implicit `None` returns
- Full strict mode compliance

Configuration in `pyproject.toml`:
```toml
[tool.mypy]
strict = true
mypy_path = "src"
```

## Project Structure

```
error-architecture/
├── pyproject.toml              # Poetry configuration with strict mypy
├── README.md                   # This file
├── src/
│   └── app/
│       ├── __init__.py         # Package exports
│       ├── exceptions.py       # Exception hierarchy
│       ├── models.py          # ErrorResponse dataclass
│       ├── mapper.py          # Error mapping logic
│       ├── decorators.py      # error_boundary decorator
│       ├── logging_config.py  # Logging setup
│       ├── cli.py            # CLI example
│       └── api_example.py    # API endpoint example
└── tests/
    └── test_errors.py         # 6 comprehensive tests
```

## Key Features

- **Production Ready**: Clean, professional code suitable for enterprise applications
- **Type Safe**: Full mypy --strict compliance with zero type: ignore comments
- **Zero Dependencies**: Uses only Python standard library (except pytest/mypy as dev deps)
- **Middleware Pipeline**: Inspired by C# middleware patterns for composable error handling
- **Immutable Responses**: Frozen dataclasses prevent accidental mutations
- **Secure**: Never leaks raw exception details in error responses
- **Tested**: 6 comprehensive pytest tests covering all error paths
- **Well Documented**: Docstrings follow Google style with examples

## Design Principles

1. **Separation of Concerns**: Exceptions, mapping, and boundaries are separate modules
2. **No Exception Re-raising**: Once caught, exceptions are converted to responses
3. **Structured Error Information**: All errors follow consistent response format
4. **Centralized Handling**: Single point of error mapping prevents inconsistencies
5. **Type Safety First**: Strict typing prevents entire categories of bugs
6. **Logging Context**: Full stack traces logged without leaking to users

## License

This is a sample project for educational purposes.
