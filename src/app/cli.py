"""
CLI example demonstrating error boundary and structured error handling.

Shows how the error handling architecture works in practical CLI applications.
"""

from app.decorators import error_boundary
from app.exceptions import ValidationError
from app.logging_config import configure_logging, get_logger
from app.models import ErrorResponse

logger = get_logger(__name__)


@error_boundary
def validate_username(username: str) -> None:
    """Validate and process a username.

    Args:
        username: The username to validate.

    Raises:
        ValidationError: If username is empty or too short.
    """
    if not username:
        raise ValidationError("Username cannot be empty")

    if len(username) < 3:
        raise ValidationError("Username must be at least 3 characters long")


def main() -> None:
    """Run the CLI example."""
    configure_logging()

    # Example 1: Valid input
    print("Example 1: Valid username")
    result1 = validate_username("john_doe")
    print(f"  Status: {result1.status}")
    print(f"  Message: {result1.message}")
    print(f"  Timestamp: {result1.timestamp}")
    print()

    # Example 2: Invalid input (too short)
    print("Example 2: Invalid username (too short)")
    result2 = validate_username("ab")
    print(f"  Status: {result2.status}")
    print(f"  Error Code: {result2.error_code}")
    print(f"  Message: {result2.message}")
    print(f"  Timestamp: {result2.timestamp}")
    print()

    # Example 3: Empty input
    print("Example 3: Empty username")
    result3 = validate_username("")
    print(f"  Status: {result3.status}")
    print(f"  Error Code: {result3.error_code}")
    print(f"  Message: {result3.message}")
    print(f"  Timestamp: {result3.timestamp}")


if __name__ == "__main__":
    main()
