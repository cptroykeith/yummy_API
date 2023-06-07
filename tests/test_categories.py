import collections
import os
import pytest
import jwt
from server import create_app
from app.service import create_category, delete_category, edit_category, get_category, get_user_categories
from app.models import Category, Recipe
from utils.http_code import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
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
        payload = {"id": 2}  # Modify the payload as needed
        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        request = MockRequest(headers={"Authorization": f"Bearer {token}"})
        # Provide a valid category ID and user ID
        # category_id = 12
        # user_id = 2
         #Create some test users
        create_category(request, {
            "name":"pillawo2",
            "description":"hot pillawo2",
            "id":1,
        })

        # Generate a sample JWT token with a secret key
        payload = {"id": 2}  # Modify the payload as needed
        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # Create a mock request object with the JWT token in the headers
        request = MockRequest(headers={"Authorization": f"Bearer {token}"})

        # Mock the Category.query.filter_by().first() method
        mock_category_query = mocker.patch.object(Category.query, "filter_by")
        mock_category_query.return_value.first.return_value = Category(
            name="pillawo2",
            description="hot pillawo2",
        )
        # import pdb; pdb.set_trace();

        # Call the get_category function with the mock request
        response = get_category(request, 33)

        assert response[0].get("status") == HTTP_200_OK
        # assert response[0].get("message") == 'Category found'

def test_get_category_not_found(mocker):
    # Create the Flask app instance
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        # Provide a non-existent category ID and user ID
        category_id = 1
        user_id = 2

        # Generate a sample JWT token with a secret key
        payload = {"id": user_id}  # Modify the payload as needed
        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # Create a mock request object with the JWT token in the headers
        request = MockRequest(headers={"Authorization": f"Bearer {token}"})

        # Mock the Category.query.filter_by().first() method to return None
        mock_category_query = mocker.patch.object(Category.query, "filter_by")
        mock_category_query.return_value.first.return_value = None

        # Call the get_category function with the mock request
        response = get_category(request, category_id)

        # Assert the response
        expected_data = None

        assert response[0].get("status") == HTTP_404_NOT_FOUND
        assert response[0].get("message"), 'Category not found' == 'Category not found'
        assert response[0].get("data") == expected_data


def test_edit_category(mocker):
    # Create the Flask app instance
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        # Provide a valid category ID and user ID
        category_id = 1
        user_id = 2

        # Generate a sample JWT token with a secret key
        payload = {"id": user_id}  # Modify the payload as needed
        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # Create a mock request object with the JWT token in the headers
        request = MockRequest(headers={"Authorization": f"Bearer {token}"})

        # Provide the updated category data
        category_data = {
            "name": "New Category Name",
            "description": "Updated category description",
        }

        # Mock the Category.query.filter_by().first() method
        mock_category_query = mocker.patch.object(Category.query, "filter_by")
        mock_category_query.return_value.first.return_value = Category(
            id=category_id,
            name="Books",
            description="Category for books",
            user_id=user_id,
        )

        # Call the edit_category function with the mock request
        response = edit_category(request, category_id, category_data)

        assert response[0].get("status"), HTTP_200_OK == HTTP_200_OK
        assert response[0].get("message"), 'Category updated' == 'Category updated'
        

def test_edit_category_not_found(mocker):
    # Create the Flask app instance
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        # Provide a non-existent category ID and user ID
        category_id = 1
        user_id = 2

        # Generate a sample JWT token with a secret key
        payload = {"id": user_id}  # Modify the payload as needed
        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # Create a mock request object with the JWT token in the headers
        request = MockRequest(headers={"Authorization": f"Bearer {token}"})

        # Provide the updated category data
        category_data = {
            "name": "New Category Name",
            "description": "Updated category description",
        }

        # Mock the Category.query.filter_by().first() method to return None
        mock_category_query = mocker.patch.object(Category.query, "filter_by")
        mock_category_query.return_value.first.return_value = None

        # Call the edit_category function with the mock request
        response = edit_category(request, category_id, category_data)

        # Assert the response
        expected_data = None

        assert response[0].get("status"), HTTP_404_NOT_FOUND== HTTP_404_NOT_FOUND
        assert response[0].get("message"),'Category not found' == 'Category not found'
        assert response[0].get("data") == expected_data


def test_delete_category(mocker):
    MockRequest = collections.namedtuple("MockRequest", ["headers", "args"])
    # Create the Flask app instance
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        # Provide a valid category ID and user ID
        category_id = 1
        user_id = 2

        # Generate a sample JWT token with a secret key
        payload = {"id": user_id}  # Modify the payload as needed
        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # Create a mock request object with the JWT token and confirmation query parameter
        request = MockRequest(headers={"Authorization": f"Bearer {token}"}, args={"confirmation": "yes"})

        # Mock the Category.query.filter_by().first() method
        mock_category_query = mocker.patch.object(Category.query, "filter_by")
        mock_category_query.return_value.first.return_value = Category(
            id=category_id,
            name="Books",
            description="Category for books",
            user_id=user_id,
        )

        # Mock the Recipe.query.options().filter_by().all() method
        mock_recipe_query = mocker.patch.object(Recipe.query, "options")
        mock_recipe_query.return_value.filter_by.return_value.all.return_value = [
            Recipe(id=1, name="Recipe 1", category_id=category_id, user_id=user_id),
            Recipe(id=2, name="Recipe 2", category_id=category_id, user_id=user_id),
        ]

        # Call the delete_category function with the mock request
        response = delete_category(request, category_id)

        # Assert the response
        assert response[0].get("status"), HTTP_200_OK == HTTP_200_OK
        assert response[0].get("message"), 'Category deleted' == 'Category deleted'

def test_delete_category_not_found(mocker):
    MockRequest = collections.namedtuple("MockRequest", ["headers", "args"])
    # Create the Flask app instance
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        # Provide a non-existent category ID and user ID
        category_id = 1
        user_id = 2

        # Generate a sample JWT token with a secret key
        payload = {"id": user_id}  # Modify the payload as needed
        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # Create a mock request object with the JWT token and confirmation query parameter
        request = MockRequest(headers={"Authorization": f"Bearer {token}"}, args={"confirmation": "yes"})

        # Mock the Category.query.filter_by().first() method to return None
        mock_category_query = mocker.patch.object(Category.query, "filter_by")
        mock_category_query.return_value.first.return_value = None

        # Call the delete_category function with the mock request
        response = delete_category(request, category_id)

        # Assert the response
        assert response[0].get("status"),HTTP_404_NOT_FOUND == HTTP_404_NOT_FOUND
        assert response[0].get("message"),'Category not found' == 'Category not found'

def test_delete_category_cancel_deletion(mocker):
    MockRequest = collections.namedtuple("MockRequest", ["headers", "args"])
    # Create the Flask app instance
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        # Provide a valid category ID and user ID
        category_id = 1
        user_id = 2

        # Generate a sample JWT token with a secret key
        payload = {"id": user_id}  # Modify the payload as needed
        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # Create a mock request object with the JWT token and confirmation query parameter
        request = MockRequest(headers={"Authorization": f"Bearer {token}"}, args={"confirmation": "no"})

        # Call the delete_category function with the mock request
        response = delete_category(request, category_id)

        # Assert the response
        assert response[0].get("status"), HTTP_200_OK == HTTP_200_OK
        assert response[0].get("message"), 'Category deletion canceled' == 'Category deletion canceled'

def test_delete_category_invalid_confirmation(mocker):
    MockRequest = collections.namedtuple("MockRequest", ["headers", "args"])
    # Create the Flask app instance
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        # Provide a valid category ID and user ID
        category_id = 1
        user_id = 2

        # Generate a sample JWT token with a secret key
        payload = {"id": user_id}  # Modify the payload as needed
        secret_key = os.environ.get("SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # Create a mock request object with the JWT token and invalid confirmation query parameter
        request = MockRequest(headers={"Authorization": f"Bearer {token}"}, args={"confirmation": "invalid"})

        # Call the delete_category function with the mock request
        response = delete_category(request, category_id)

        # Assert the response
        assert response[0].get("status"),HTTP_400_BAD_REQUEST == HTTP_400_BAD_REQUEST
        assert response[0].get("message"), "Please confirm deletion by providing 'confirmation=yes' query parameter or 'confirmation=no' to cancel deletion" == "Please confirm deletion by providing 'confirmation=yes' query parameter or 'confirmation=no' to cancel deletion"
