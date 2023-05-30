import collections
import os
import pytest
import jwt
from server import create_app
from users.service import create_recipe
from users.models import Recipe
from utils.http_code import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from unittest.mock import patch, MagicMock

MockRequest = collections.namedtuple("MockRequest", ["headers"])

def test_create_recipe(mocker):
    # Create the Flask app instance
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        # Provide valid recipe data
        recipe_data = {
            "name": "Chocolate Cake",
            "description": "Delicious chocolate cake recipe",
            "category_id": 1
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
            mock_recipe = MagicMock()
            mock_session.return_value = mock_session
            mock_session.add.return_value = None
            mock_session.commit.return_value = None
            mock_db.Recipe = mock_recipe

            # Call the create_recipe function with the mock request
            response = create_recipe(request, recipe_data)

        # Assert the response
        assert response[0].get("status"), HTTP_201_CREATED == HTTP_201_CREATED
        assert response[0].get("message"),'Recipe created' == 'Recipe created'
        

