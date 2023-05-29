import os
import pytest
import jwt
from server import create_app
from users.service import create_category
from utils.http_code import HTTP_201_CREATED
import collections


@pytest.fixture
def client():
    """Create a test client using the Flask application instance."""
    app = create_app()
    app.config["TESTING"] = True  # Set the app to testing mode
    with app.test_client() as client:
        with app.app_context():
            yield client


MockRequest = collections.namedtuple("MockRequest", ["headers"])

def test_create_category(client):
    # Provide valid category data
    category_data = {
        "name": "Books",
        "description": "Category for books"
    }

    # Generate a sample JWT token with a secret key
    payload = {"id": 2}  # Modify the payload as needed
    secret_key = os.environ.get("SECRET_KEY")
    token = jwt.encode(payload, secret_key,algorithm="HS256")

    # Create a mock request object with the JWT token in the headers
    print('token here', token,type(token))
    request = MockRequest(headers={"Authorization": f"Bearer {token}"})
    headers={"Authorization": f"Bearer {token}"}

    # Call the create_category function with the mock request
    response = create_category(request, category_data)

    # Assert the response
    assert response[0].get("status"), HTTP_201_CREATED == HTTP_201_CREATED
    assert response[0].get("message"), 'Category Created' ==  "Category created"

    print("response",response[0])
    # Assert the returned data matches the provided category data
    assert response[0].get("token") == category_data
    #assert response[0].get("description") == category_data["description"]
