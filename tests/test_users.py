# tests/test_users.py
# Test cases for the /users endpoint of JSONPlaceholder API
#
# Endpoints covered:
#   GET    /users          - Retrieve all users
#   GET    /users/{id}     - Retrieve a single user
#   GET    /users/9999     - Retrieve a non-existent user (negative test)
#   POST   /users          - Create a new user
#   GET    /users/{id}/posts - Retrieve posts belonging to a user

import requests
import re


# ── TEST 1 ──────────────────────────────────────────────────────────────────
def test_get_all_users_status_200(base_url):
    """
    Test: GET /users
    Expected: Status 200, response is a non-empty list of 10 users
    Type: Positive
    """
    response = requests.get(f"{base_url}/users")

    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )

    data = response.json()
    assert isinstance(data, list), "Expected response to be a list"
    assert len(data) == 10, f"Expected 10 users, got {len(data)}"


# ── TEST 2 ──────────────────────────────────────────────────────────────────
def test_get_single_user_has_valid_email(base_url, valid_user_id):
    """
    Test: GET /users/1
    Expected: Status 200, user has valid email format, required fields present
    Type: Positive
    """
    response = requests.get(f"{base_url}/users/{valid_user_id}")

    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )

    data = response.json()

    # Verify required fields exist
    assert "name" in data and data["name"] != "", "User name is missing or empty"
    assert "username" in data and data["username"] != "", "Username is missing or empty"
    assert "email" in data, "Email field is missing"

    # Verify email format using regex
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    assert re.match(email_pattern, data["email"]), (
        f"Invalid email format: {data['email']}"
    )

    # Verify nested address field exists
    assert "address" in data, "Address field is missing"
    assert "city" in data["address"], "City field missing in address"


# ── TEST 3 ──────────────────────────────────────────────────────────────────
def test_get_nonexistent_user_returns_404(base_url, invalid_id):
    """
    Test: GET /users/9999
    Expected: Status 404 (user does not exist)
    Type: Negative
    """
    response = requests.get(f"{base_url}/users/{invalid_id}")

    assert response.status_code == 404, (
        f"Expected status 404 for invalid user ID, got {response.status_code}"
    )


# ── TEST 4 ──────────────────────────────────────────────────────────────────
def test_create_user_returns_201(base_url, new_user_payload):
    """
    Test: POST /users
    Expected: Status 201, response contains sent data plus a new ID
    Type: Positive
    """
    response = requests.post(f"{base_url}/users", json=new_user_payload)

    assert response.status_code == 201, (
        f"Expected status 201, got {response.status_code}"
    )

    data = response.json()

    # Verify the response reflects the sent payload
    assert data["name"] == new_user_payload["name"], (
        f"Expected name '{new_user_payload['name']}', got '{data['name']}'"
    )
    assert data["email"] == new_user_payload["email"], (
        f"Expected email '{new_user_payload['email']}', got '{data['email']}'"
    )

    # Verify a new ID was assigned
    assert "id" in data, "Response is missing the 'id' field"


# ── TEST 5 ──────────────────────────────────────────────────────────────────
def test_get_posts_by_user_not_empty(base_url, valid_user_id):
    """
    Test: GET /users/1/posts
    Expected: Status 200, user has at least one post
    Type: Positive
    """
    response = requests.get(f"{base_url}/users/{valid_user_id}/posts")

    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )

    data = response.json()
    assert isinstance(data, list), "Expected response to be a list"
    assert len(data) > 0, f"Expected user {valid_user_id} to have at least one post"

    # Verify all posts belong to the correct user
    for post in data:
        assert post["userId"] == valid_user_id, (
            f"Post userId {post['userId']} does not match expected userId {valid_user_id}"
        )

def test_get_user_with_invalid_string_id(base_url):
    """Negative test: GET user with invalid string ID should return 404."""
    response = requests.get(f"{base_url}/users/invalid-id")
    assert response.status_code == 404
