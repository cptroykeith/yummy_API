import collections
from flask import request
import pytest
from server import create_app
from app.models import User
from app.service import create_user, delete_user, get_all_users, get_user_by_id, login_user
from utils.http_code import HTTP_200_OK, HTTP_201_CREATED
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    """Create a test client using the Flask application instance."""
    app = create_app()
    app.config["TESTING"] = True  # Set the app to testing mode
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_create_user():
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response = create_user(None, user_data)
    if isinstance(response, tuple) and "error" in response[0] and response[0]["error"] == "Username already exist":
        assert response[0]["error"] == "Username already exist"
    else:
        assert response[0].get("message"), 'User Created' == "User Created"

def test_login_user(client):
    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    response = login_user(None, user_data)
    assert response[0].get("message"),"User login successfully" == "User login successfully"
    assert response[0].get("status"), HTTP_201_CREATED == HTTP_201_CREATED

MockRequest = collections.namedtuple("MockRequest", ["headers"])

def test_get_all_users(mocker):
    # Create some test users
    create_user(None, {
        "username": "user1",
        "email": "user1@example.com",
        "password": "password1"
    })
    create_user(None, {
        "username": "user2",
        "email": "user2@example.com",
        "password": "password2"
    })
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        mock_user_query = mocker.patch.object(User.query, "filter_by")
        mock_user_query.return_value.all.return_value = [
            User(id=1,username="user1", email="user1@example.com", password="password1"),
            User(id=2,username="user1", email="user2@example.com", password="password2"),
        ]

    # Call the get_all_users endpoint
    response = get_all_users()

    # Assert the response
    assert response[0].status ,HTTP_200_OK == HTTP_200_OK
    assert response[0].json['message'] == "All users retrieved"


def test_get_user_by_id(client):
    # Create a test user
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    create_user(None, user_data)

    # Get the user ID
    user_id = 2

    # Call the get_user_by_id endpoint
    response = get_user_by_id(None, user_id)

    # Assert the response
    assert response[0].get("status"), HTTP_200_OK == HTTP_200_OK
    assert response[0].get("message"),"User retrieved successfully" == "User retrieved successfully"

# def test_delete_user(client):
#     # Create a test user
#     user_data = {
#         "username": "testuser",
#         "email": "testuser@example.com",
#         "password": "testpassword"
#     }
#     create_user(None, user_data)

#     # Get the user ID
#     user_id = 1

#     # Call the delete_user endpoint
#     response = delete_user(None, user_id)

#     # Assert the response
#     assert response[0].get("status") == HTTP_200_OK
#     assert response[0].get("message") == "User deleted"

#     # Try to retrieve the user after deletion
#     deleted_user = User.query.get(user_id)

#     # Assert that the user is None, indicating deletion
#     assert deleted_user is None

    
