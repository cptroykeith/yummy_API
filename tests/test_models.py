from flask_bcrypt import generate_password_hash, check_password_hash
from users.models import User, Category, Recipe

# Test User class
def test_user():
    # Generate a valid password hash
    password_hash = generate_password_hash('password').decode('utf-8')

    # Create a User instance
    user = User(username='testuser', email='test@example.com', password=password_hash)

    # Test initialization
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert check_password_hash(user.password, 'password')

    # Test __repr__
    assert repr(user) == '<User testuser>'

    # Test check_password
    assert user.check_password('password') is True
    assert user.check_password('wrong_password') is False

# Test Category class
def test_category():
    # Create a Category instance
    category = Category(name='Test Category', description='This is a test category')

    # Test initialization
    assert category.name == 'Test Category'
    assert category.description == 'This is a test category'

    # Test __repr__
    assert repr(category) == '<Category Test Category>'

    # Test to_dict
    category_dict = category.to_dict()
    assert category_dict == {
        'id': None,
        'name': 'Test Category',
        'description': 'This is a test category',
        'user_id': None,
    }

# Test Recipe class
def test_recipe():
    # Create a Recipe instance
    recipe = Recipe(
        type='Test Recipe',
        ingredients='Ingredient 1, Ingredient 2',
        steps='Step 1, Step 2',
        category_id=1
    )

    # Test initialization
    assert recipe.type == 'Test Recipe'
    assert recipe.ingredients == 'Ingredient 1, Ingredient 2'
    assert recipe.steps == 'Step 1, Step 2'
    assert recipe.category_id == 1

    # Test __repr__
    assert repr(recipe) == '<Recipe Test Recipe>'

    # Test to_dict
    recipe_dict = recipe.to_dict()
    assert recipe_dict == {
        'id': None,
        'type': 'Test Recipe',
        'ingredients': 'Ingredient 1, Ingredient 2',
        'steps': 'Step 1, Step 2',
        'user_id': None,
        'category_id': 1,
    }
