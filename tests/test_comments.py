# tests/test_comments.py
# Test cases for the /comments endpoint of JSONPlaceholder API
#
# Endpoints covered:
#   GET    /comments              - Retrieve all comments
#   GET    /comments?postId={id}  - Retrieve comments filtered by postId
#   GET    /comments/9999         - Retrieve a non-existent comment (negative test)
#   GET    /comments/{id}         - Validate comment email format

import requests
import re


# ── TEST 1 ──────────────────────────────────────────────────────────────────
def test_get_all_comments_status_200(base_url):
    """
    Test: GET /comments
    Expected: Status 200, response is a non-empty list
    Type: Positive
    """
    response = requests.get(f"{base_url}/comments")

    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )

    data = response.json()
    assert isinstance(data, list), "Expected response to be a list"
    assert len(data) > 0, "Expected at least one comment in the response"


# ── TEST 2 ──────────────────────────────────────────────────────────────────
def test_get_comments_filtered_by_post_id(base_url, valid_post_id):
    """
    Test: GET /comments?postId=1
    Expected: Status 200, all returned comments belong to the correct postId
    Type: Positive
    """
    response = requests.get(
        f"{base_url}/comments",
        params={"postId": valid_post_id}
    )

    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )

    data = response.json()
    assert isinstance(data, list), "Expected response to be a list"
    assert len(data) > 0, f"Expected comments for postId {valid_post_id}"

    # Verify every comment belongs to the correct post
    for comment in data:
        assert comment["postId"] == valid_post_id, (
            f"Comment postId {comment['postId']} does not match "
            f"expected postId {valid_post_id}"
        )


# ── TEST 3 ──────────────────────────────────────────────────────────────────
def test_get_nonexistent_comment_returns_404(base_url, invalid_id):
    """
    Test: GET /comments/9999
    Expected: Status 404 (comment does not exist)
    Type: Negative
    """
    response = requests.get(f"{base_url}/comments/{invalid_id}")

    assert response.status_code == 404, (
        f"Expected status 404 for invalid comment ID, got {response.status_code}"
    )


# ── TEST 4 ──────────────────────────────────────────────────────────────────
def test_comment_email_format_is_valid(base_url, valid_comment_id):
    """
    Test: GET /comments/1
    Expected: Status 200, comment email field has valid format,
              all required fields present
    Type: Positive
    """
    response = requests.get(f"{base_url}/comments/{valid_comment_id}")

    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )

    data = response.json()

    # Verify required fields
    assert "postId" in data, "postId field is missing"
    assert "id" in data, "id field is missing"
    assert "name" in data and data["name"] != "", "name is missing or empty"
    assert "body" in data and data["body"] != "", "body is missing or empty"
    assert "email" in data, "email field is missing"

    # Validate email format
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    assert re.match(email_pattern, data["email"]), (
        f"Invalid email format in comment: {data['email']}"
    )
