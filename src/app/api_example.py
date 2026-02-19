"""
API example demonstrating error boundary in endpoint-style functions.

Shows how the error handling architecture integrates with API endpoint
handlers.
"""

from app.decorators import error_boundary
from app.exceptions import NotFoundError
from app.models import ErrorResponse


# Simulated database
_USERS_DB = {
    1: {"id": 1, "name": "Alice"},
    2: {"id": 2, "name": "Bob"},
    3: {"id": 3, "name": "Charlie"},
}


@error_boundary
def get_user(user_id: int) -> None:
    """Simulated API endpoint to fetch a user.

    Args:
        user_id: The ID of the user to fetch.

    Raises:
        NotFoundError: If user with given ID doesn't exist.
    """
    if user_id not in _USERS_DB:
        raise NotFoundError(f"User with ID {user_id} not found")

    user = _USERS_DB[user_id]


def demo_api() -> None:
    """Run the API example."""
    print("API Example: Fetching users")
    print()

    # Example 1: Existing user
    print("Request: GET /users/1")
    response = get_user(1)
    print(f"  Status: {response.status}")
    print(f"  Message: {response.message}")
    print()

    # Example 2: Non-existent user
    print("Request: GET /users/999")
    response = get_user(999)
    print(f"  Status: {response.status}")
    print(f"  Error Code: {response.error_code}")
    print(f"  Message: {response.message}")


if __name__ == "__main__":
    demo_api()
