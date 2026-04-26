# tests/test_posts.py
# Test cases for the /posts endpoint of JSONPlaceholder API
#
# Endpoints covered:
#   GET    /posts          - Retrieve all posts
#   GET    /posts/{id}     - Retrieve a single post
#   GET    /posts/9999     - Retrieve a non-existent post (negative test)
#   POST   /posts          - Create a new post
#   PUT    /posts/{id}     - Update an existing post
#   DELETE /posts/{id}     - Delete a post

import requests


# ── TEST 1 ──────────────────────────────────────────────────────────────────
def test_get_all_posts_status_200(base_url):
    """
    Test: GET /posts
    Expected: Status 200, response is a non-empty list
    Type: Positive
    """
    response = requests.get(f"{base_url}/posts")

    # Verify HTTP status code
    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )

    # Verify response is a list and not empty
    data = response.json()
    assert isinstance(data, list), "Expected response to be a list"
    assert len(data) > 0, "Expected at least one post in the response"


# ── TEST 2 ──────────────────────────────────────────────────────────────────
def test_get_single_post_returns_correct_id(base_url, valid_post_id):
    """
    Test: GET /posts/1
    Expected: Status 200, returned post has correct ID, title and body exist
    Type: Positive
    """
    response = requests.get(f"{base_url}/posts/{valid_post_id}")

    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )

    data = response.json()

    # Verify the correct post is returned
    assert data["id"] == valid_post_id, (
        f"Expected post ID {valid_post_id}, got {data['id']}"
    )

    # Verify required fields exist and are not empty
    assert "title" in data and data["title"] != "", "Post title is missing or empty"
    assert "body" in data and data["body"] != "", "Post body is missing or empty"
    assert "userId" in data, "Post userId field is missing"


# ── TEST 3 ──────────────────────────────────────────────────────────────────
def test_get_nonexistent_post_returns_404(base_url, invalid_id):
    """
    Test: GET /posts/9999
    Expected: Status 404 (post does not exist)
    Type: Negative
    """
    response = requests.get(f"{base_url}/posts/{invalid_id}")

    assert response.status_code == 404, (
        f"Expected status 404 for invalid ID, got {response.status_code}"
    )


# ── TEST 4 ──────────────────────────────────────────────────────────────────
def test_create_post_returns_201(base_url, new_post_payload):
    """
    Test: POST /posts
    Expected: Status 201, response contains sent data plus a new ID
    Type: Positive
    """
    response = requests.post(f"{base_url}/posts", json=new_post_payload)

    assert response.status_code == 201, (
        f"Expected status 201, got {response.status_code}"
    )

    data = response.json()

    # Verify the response reflects the sent payload
    assert data["title"] == new_post_payload["title"], (
        f"Expected title '{new_post_payload['title']}', got '{data['title']}'"
    )
    assert data["body"] == new_post_payload["body"], (
        f"Expected body '{new_post_payload['body']}', got '{data['body']}'"
    )
    assert data["userId"] == new_post_payload["userId"], (
        f"Expected userId {new_post_payload['userId']}, got {data['userId']}"
    )

    # Verify a new ID was assigned
    assert "id" in data, "Response is missing the 'id' field"
    assert isinstance(data["id"], int), "Expected 'id' to be an integer"


# ── TEST 5 ──────────────────────────────────────────────────────────────────
def test_update_post_returns_200(base_url, valid_post_id):
    """
    Test: PUT /posts/1
    Expected: Status 200, response reflects updated data
    Type: Positive
    """
    updated_payload = {
        "id": valid_post_id,
        "title": "Updated Title",
        "body": "Updated body content.",
        "userId": 1
    }

    response = requests.put(
        f"{base_url}/posts/{valid_post_id}",
        json=updated_payload
    )

    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )

    data = response.json()

    # Verify updated fields are reflected in the response
    assert data["title"] == updated_payload["title"], (
        f"Expected updated title '{updated_payload['title']}', got '{data['title']}'"
    )
    assert data["body"] == updated_payload["body"], (
        f"Expected updated body '{updated_payload['body']}', got '{data['body']}'"
    )


# ── TEST 6 ──────────────────────────────────────────────────────────────────
def test_delete_post_returns_200(base_url, valid_post_id):
    """
    Test: DELETE /posts/1
    Expected: Status 200, response body is empty object
    Type: Positive
    """
    response = requests.delete(f"{base_url}/posts/{valid_post_id}")

    assert response.status_code == 200, (
        f"Expected status 200, got {response.status_code}"
    )

    # JSONPlaceholder returns empty object {} on successful delete
    data = response.json()
    assert data == {}, (
        f"Expected empty object after delete, got {data}"
    )

def test_get_post_with_invalid_string_id(base_url):
    """Negative test: GET post with invalid string ID should return 404."""
    response = requests.get(f"{base_url}/posts/invalid-id")
    assert response.status_code == 404