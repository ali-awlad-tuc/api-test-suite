# conftest.py
# Shared configuration and fixtures for all test modules
# JSONPlaceholder API: https://jsonplaceholder.typicode.com

import pytest

# Base URL used by all tests
BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture
def base_url():
    """Returns the base URL for the API."""
    return BASE_URL


@pytest.fixture
def valid_post_id():
    """A known valid post ID."""
    return 1


@pytest.fixture
def valid_user_id():
    """A known valid user ID."""
    return 1


@pytest.fixture
def valid_comment_id():
    """A known valid comment ID."""
    return 1


@pytest.fixture
def invalid_id():
    """An ID that does not exist in the API."""
    return 9999


@pytest.fixture
def new_post_payload():
    """Sample payload for creating a new post."""
    return {
        "title": "Test Post Title",
        "body": "This is the body of the test post.",
        "userId": 1
    }


@pytest.fixture
def new_user_payload():
    """Sample payload for creating a new user."""
    return {
        "name": "Ali Awlad",
        "username": "aliawlad",
        "email": "testuser@example.com"
    }
