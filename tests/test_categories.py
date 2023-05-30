import collections
import os
import pytest
import jwt
from server import create_app
from users.service import create_category
from utils.http_code import HTTP_201_CREATED
from unittest.mock import patch, MagicMock

MockRequest = collections.namedtuple("MockRequest", ["headers"])

def test_create_category(mocker):
    # Create the Flask app instance
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        # Provide valid category data
        category_data = {
            "name": "Books",
            "description": "Category for books"
        }
        os.environ["SECRET_KEY"] = 'this is a secret key'

        # Generate a sample JWT token with a secret key
        payload = {"id": 2}  # Modify the payload as needed
        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # Create a mock request object with the JWT token in the headers
        request = MockRequest(headers={"Authorization": f"Bearer {token}"})

        # Mock the database interaction
        with patch("users.service.db") as mock_db:
            mock_session = mock_db.session
            mock_category = MagicMock()
            mock_session.return_value = mock_session
            mock_session.add.return_value = None
            mock_session.commit.return_value = None
            mock_db.Category = mock_category

            # Call the create_category function with the mock request
            response = create_category(request, category_data)

        # Assert the response
        assert response[0].get("status") == HTTP_201_CREATED
        assert response[0].get("message") == 'Category created'
        #assert response[0].get("data") == category_data
