import collections
import os
import pytest
import jwt
from server import create_app
from users.service import create_category, get_category, get_user_categories
from users.models import Category
from utils.http_code import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
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

def test_get_user_categories(mocker):
    # Create the Flask app instance
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        # Create a mock request object with a valid JWT token in the headers
        token_payload = {"id": 2}  # Modify the payload as needed
        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(token_payload, secret_key, algorithm="HS256")
        request = MockRequest(headers={"Authorization": f"Bearer {token}"})

        # Mock the Category.query.filter_by().all() method
        mock_category_query = mocker.patch.object(Category.query, "filter_by")
        mock_category_query.return_value.all.return_value = [
            Category(id=1, name="Books", user_id=2),
            Category(id=2, name="Movies", user_id=2),
        ]

        # Call the get_user_categories function with the mock request
        response = get_user_categories(request)

        assert response[0].get("status") == HTTP_200_OK
        assert response[0].get("message") == 'Categories retrieved'

def test_get_category(mocker):
    # Create the Flask app instance
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        # Provide a valid category ID and user ID
        category_id = 12
        user_id = 2

        # Generate a sample JWT token with a secret key
        payload = {"id": user_id}  # Modify the payload as needed
        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # Create a mock request object with the JWT token in the headers
        request = MockRequest(headers={"Authorization": f"Bearer {token}"})

        # Mock the Category.query.filter_by().first() method
        mock_category_query = mocker.patch.object(Category.query, "filter_by")
        mock_category_query.return_value.first.return_value = Category(
            id=category_id,
            name="pillawo2",
            description="hot pillawo2",
            user_id=user_id,
        )

        # Call the get_category function with the mock request
        response = get_category(request, category_id)

        assert response[0].get("status") == HTTP_200_OK
        assert response[0].get("message") == 'Category found'
        
