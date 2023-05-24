import pytest
from server import create_app
from users.service import create_user, login_user
from utils.http_code import HTTP_201_CREATED

@pytest.fixture
def client():
    """Create a test client using the Flask application instance."""
    app = create_app()
    app.config["TESTING"] = True  # Set the app to testing mode
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_create_user(client):
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

def get_all_users():
    