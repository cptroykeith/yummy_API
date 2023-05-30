import collections
import os
import pytest
import jwt
from server import create_app
from users.service import create_recipe, get_recipe_by_id, get_recipes_by_category
from users.models import Recipe
from utils.http_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
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
        
@pytest.fixture(scope="module")
def app():
    # Create the Flask app instance
    app = create_app()
    app.app_context().push()
    yield app

def test_get_recipes_by_category(app, mocker):
    # Provide a sample user ID and category ID
    user_id = 2
    category_id = 1

    # Mock the Recipe.query.filter_by().all() method
    mock_recipe_query = mocker.patch.object(Recipe.query, "filter_by")
    mock_recipe_query.return_value.all.return_value = [
        Recipe(name="Recipe 1", description="Recipe 1 description"),
        Recipe(name="Recipe 2", description="Recipe 2 description"),
    ]

    # Call the get_recipes_by_category function
    response = get_recipes_by_category(user_id, category_id)

    assert response[0].get("status"), HTTP_200_OK == HTTP_200_OK
    assert response[0].get("message"),"Recipes retrieved successfully" == "Recipes retrieved successfully"

def test_get_recipes_by_category_no_recipes(mocker):
    # Provide a sample user ID and category ID
    user_id = 2
    category_id = 1

    # Mock the Recipe.query.filter_by().all() method to return an empty list
    mock_recipe_query = mocker.patch.object(Recipe.query, "filter_by")
    mock_recipe_query.return_value.all.return_value = []

    # Call the get_recipes_by_category function
    response = get_recipes_by_category(user_id, category_id)

    # Assert the response
    assert response[0].get("status"),HTTP_404_NOT_FOUND == HTTP_404_NOT_FOUND
    assert response[0].get("message"), "No recipes found for the given user and category" == "No recipes found for the given user and category"
    assert response[0].get("data") is None


def test_get_recipe_by_id():
    # Create the Flask app instance
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        # Provide valid user ID, category ID, and recipe ID
        user_id = 1
        category_id = 2
        recipe_id = 3

        # Mock the Recipe.query.filter_by method
        with patch("users.service.Recipe.query.filter_by") as mock_query:
            # Mock the Recipe object returned by the query
            mock_recipe = Recipe(id=recipe_id, user_id=user_id, category_id=category_id)
            mock_query.return_value.first.return_value = mock_recipe

            # Call the get_recipe_by_id function
            response = get_recipe_by_id(user_id, category_id, recipe_id)

        # Assert the response
        assert response[0].get("status"),HTTP_200_OK == HTTP_200_OK
        assert response[0].get("message"), 'Recipe retrieved successfully' == 'Recipe retrieved successfully'

def test_get_recipe_by_id_recipe_not_found():
    # Create the Flask app instance
    app = create_app()

    # Use the app context for the test
    with app.app_context():
        # Provide valid user ID, category ID, and recipe ID
        user_id = 1
        category_id = 2
        recipe_id = 3

        # Mock the Recipe.query.filter_by method
        with patch("users.service.Recipe.query.filter_by") as mock_query:
            # Mock the Recipe object returned by the query as None (recipe not found)
            mock_query.return_value.first.return_value = None

            # Call the get_recipe_by_id function
            response = get_recipe_by_id(user_id, category_id, recipe_id)

        # Assert the response
        assert response[0].get("status"),HTTP_404_NOT_FOUND == HTTP_404_NOT_FOUND
        assert response[0].get("message"),'Recipe not found' == 'Recipe not found'
        assert response[0].get("data") is None

