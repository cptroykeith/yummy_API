import json
from flask import jsonify
import jwt
import datetime
from server import db
from os import environ
from app.helper import send_forgot_password_email
from app.models import User, Category, Recipe
from flask_bcrypt import generate_password_hash
from utils.common import generate_response, TokenGenerator
from sqlalchemy.orm import joinedload
from .validation import (
    CreateLoginInputSchema,
    CreateResetPasswordEmailSendInputSchema,
    CreateSignupInputSchema, ResetPasswordInputSchema, CreateCategoryInputSchema, CreateRecipeInputSchema
)
from utils.http_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT

def create_user(request, input_data):

    create_validation_schema = CreateSignupInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    check_username_exist = User.query.filter_by(
        username=input_data.get("username")
    ).first()
    check_email_exist = User.query.filter_by(email=input_data.get("email")).first()
    if check_username_exist:
        return generate_response(
            message="Username already exist", status=HTTP_409_CONFLICT
        )
    elif check_email_exist:
        return generate_response(
            message="Email  already taken", status=HTTP_400_BAD_REQUEST
        )

    new_user = User(**input_data)  # Create an instance of the User class
    new_user.hash_password()
    db.session.add(new_user)  # Adds new User record to database
    db.session.commit()  # Comment
    del input_data["password"]
    return generate_response(
        data=input_data, message="User Created", status=HTTP_201_CREATED
    )

def get_all_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
        user_list.append(user_data)

    response_data = {
        "data": user_list,
        "message": "All users retrieved"
    }
    return jsonify(response_data), HTTP_200_OK

def get_user_by_id(request, user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return generate_response(message="User not found", status=HTTP_404_NOT_FOUND)
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
    return generate_response(data=user_data, message="User retrieved successfully", status=HTTP_200_OK)

def delete_user(request, user_id: int):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return generate_response(message="User not found", status=HTTP_404_NOT_FOUND)
    db.session.delete(user)
    db.session.commit()
    return generate_response(message="User deleted", status=HTTP_200_OK)


def login_user(request, input_data):
    
    create_validation_schema = CreateLoginInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)

    get_user = User.query.filter_by(email=input_data.get("email")).first()
    if get_user is None:
        return generate_response(message="User not found", status=HTTP_400_BAD_REQUEST)
    if get_user.check_password(input_data.get("password")):
        token = jwt.encode(
            {
                "id": get_user.id,
                "email": get_user.email,
                "username": get_user.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            },
            environ.get("SECRET_KEY"),
        )
        input_data["token"] = token
        return generate_response(
            data = token, message="User login successfully", status=HTTP_201_CREATED
        )
    else:
        return generate_response(
            message="Password is wrong", status=HTTP_400_BAD_REQUEST
        )


def reset_password_email_send(request, input_data):
    
    create_validation_schema = CreateResetPasswordEmailSendInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    user = User.query.filter_by(email=input_data.get("email")).first()
    if user is None:
        return generate_response(
            message="No record found with this email. please signup first.",
            status=HTTP_400_BAD_REQUEST,
        )
    send_forgot_password_email(request, user)
    return generate_response(
        message="Link sent to the registered email address.", status=HTTP_200_OK
    )


def reset_password(request, input_data, token):
    create_validation_schema = ResetPasswordInputSchema()
    errors = create_validation_schema.validate(input_data)
    if errors:
        return generate_response(message=errors)
    if not token:
        return generate_response(
            message="Token is required!",
            status=HTTP_400_BAD_REQUEST,
        )
    token = TokenGenerator.decode_token(token)
    user = User.query.filter_by(id=token.get('id')).first()
    if user is None:
        return generate_response(
            message="No record found with this email. please signup first.",
            status=HTTP_400_BAD_REQUEST,
        )
    user = User.query.filter_by(id=token['id']).first()
    user.password = generate_password_hash(input_data.get('password')).decode("utf8")
    db.session.commit()
    return generate_response(
        message="New password SuccessFully set.", status=HTTP_200_OK
    )

# categories

def create_category(request, category_data):
    # Validate category data using CreateCategoryInputSchema
    create_validation_schema = CreateCategoryInputSchema()
    errors = create_validation_schema.validate(category_data)
    if errors:
        return generate_response(message=errors)
    
    # Check if the Authorization header is present
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        print("Authorization header is missing")
        return generate_response(message="Authorization header is missing", status=HTTP_401_UNAUTHORIZED)

    print("Authorization header value:", auth_header)


    # Get user ID from token in request headers 
    token = request.headers.get('Authorization').split(' ')[-1]
    decoded_token = TokenGenerator.decode_token(token)
    user_id = decoded_token.get('id')

    # Check if the category already exists
    existing_category = Category.query.filter_by(name=category_data['name'], user_id=user_id).first()
    if existing_category:
        return generate_response(message="Category already exists", status=HTTP_400_BAD_REQUEST)
    
    # Create new category with user ID
    new_category = Category(**category_data)
    new_category.user_id = user_id
    db.session.add(new_category)
    db.session.commit()

    return generate_response(data=category_data, message="Category created", status=HTTP_201_CREATED)

#Get all categories for a user
def get_user_categories(request):
    # Get user ID from token in request headers
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_token = TokenGenerator.decode_token(token)
    user_id = decoded_token.get('id')

    # Get all categories for user ID
    categories = Category.query.filter_by(user_id=user_id).all()

    # Serialize categories using CategorySchema
    category_schema = CreateCategoryInputSchema(many=True)
    categories_data = category_schema.dump(categories)

    return generate_response(data=categories_data, message="Categories retrieved", status=HTTP_200_OK)

#Get one category for a user
def get_category(request, category_id):
    # Get user ID from token in request headers
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_token = TokenGenerator.decode_token(token)
    user_id = decoded_token.get('id')

    # Query the category with the specified ID for the user
    category = Category.query.filter_by(id=category_id, user_id=user_id).first()

    if not category:
        return generate_response(message="Category not found", status=HTTP_404_NOT_FOUND)

    # Convert the category object to a dictionary
    category_data = category.to_dict()

    return generate_response(data=category_data, message="Category found", status=HTTP_200_OK)

#Edit a category
def edit_category(request, category_id, category_data):
    # Validate category data using EditCategoryInputSchema
    edit_validation_schema = CreateCategoryInputSchema()
    errors = edit_validation_schema.validate(category_data)
    if errors:
        return generate_response(message=errors)

    # Get user ID from token in request headers
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_token = TokenGenerator.decode_token(token)
    user_id = decoded_token.get('id')

    # Query the category with the specified ID for the user
    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
    if not category:
        return generate_response(message="Category not found", status=HTTP_404_NOT_FOUND)

    # Update the category record with the new data
    category.name = category_data.get("name")
    category.description = category_data.get("description")
    db.session.commit()

    # Convert the category object to a dictionary
    category_data = category.to_dict()

    return generate_response(data=category_data, message="Category updated", status=HTTP_200_OK)

#Delete a category
def delete_category(request, category_id):
    # Get user ID from token in request headers
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_token = TokenGenerator.decode_token(token)
    user_id = decoded_token.get('id')

    # Query the category with the specified ID for the user
    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
    if not category:
        return generate_response(message="Category not found", status=HTTP_404_NOT_FOUND)
    
    # Ask for user confirmation
    confirmation = request.args.get('confirmation')

    if not confirmation or confirmation.lower() not in ['yes', 'no']:
        return generate_response(message="Please confirm deletion by providing 'confirmation=yes' query parameter or 'confirmation=no' to cancel deletion", status=HTTP_400_BAD_REQUEST)

    if confirmation.lower() == 'no':
        return generate_response(message="Category deletion canceled", status=HTTP_200_OK)

    # Delete the recipes associated with the category and user
    recipes = Recipe.query.options(joinedload('category')).filter_by(category_id=category_id, user_id=user_id).all()
    for recipe in recipes:
        db.session.delete(recipe)
    db.session.commit()
    
    # Delete the category from the database
    db.session.delete(category)
    db.session.commit()

    return generate_response(message="Category deleted", status=HTTP_200_OK)


#Recipes

#Create Recipe

def create_recipe(request, recipe_data):
    # Validate recipe data using a validation schema
    create_validation_schema = CreateRecipeInputSchema()
    errors = create_validation_schema.validate(recipe_data)
    if errors:
        return generate_response(message=errors)

    # Get user ID from token in request headers
    token = request.headers.get('Authorization')
    decoded_token = TokenGenerator.decode_token(token)
    user_id = decoded_token.get('id')

    # Get category ID from recipe_data or other source if needed
    category_id = recipe_data.get('category_id')

    # Check if the recipe already exists for the given user and category
    existing_recipe = Recipe.query.filter_by(type=recipe_data.get('type')).first()
    if existing_recipe:
        return generate_response(
            message="Recipe already exists for the given user and category",
            status=HTTP_400_BAD_REQUEST
        )

    # Create new recipe with user ID and category ID
    new_recipe = Recipe(**recipe_data)
    new_recipe.user_id = user_id
    new_recipe.category_id = category_id
    db.session.add(new_recipe)
    db.session.commit()

    return generate_response(data=recipe_data, message="Recipe created", status=HTTP_201_CREATED)


# Getting all recipes for a particular category and user

def get_recipes_by_category(user_id, category_id):
    recipes = Recipe.query.filter_by(user_id=user_id, category_id=category_id).all()
    
    if not recipes:
        return generate_response(message="No recipes found for the given user and category", status=HTTP_404_NOT_FOUND)
    
    recipe_data = [recipe.to_dict() for recipe in recipes]
    return generate_response(data=recipe_data, message="Recipes retrieved successfully", status=HTTP_200_OK)

# Get one recipe from recipe table

def get_recipe_by_id(user_id, category_id, recipe_id):
    recipe = Recipe.query.filter_by(user_id=user_id, category_id=category_id, id=recipe_id).first()

    if not recipe:
        return generate_response(message="Recipe not found", status=HTTP_404_NOT_FOUND)

    recipe_data = recipe.to_dict()
    return generate_response(data=recipe_data, message="Recipe retrieved successfully", status=HTTP_200_OK)

#Editing a recipe
def edit_recipe(request, category_id, recipe_id, recipe_data):
    # Validate recipe data using a validation schema
    edit_validation_schema = CreateRecipeInputSchema()
    errors = edit_validation_schema.validate(recipe_data)
    if errors:
        return generate_response(message=errors)

    # Get user ID from token in request headers
    token = request.headers.get('Authorization')
    decoded_token = TokenGenerator.decode_token(token)
    user_id = decoded_token.get('id')

    # Retrieve the recipe to be edited
    recipe = Recipe.query.filter_by(id=recipe_id, category_id=category_id, user_id=user_id).first()
    if not recipe:
        return generate_response(message="Recipe not found", status=HTTP_404_NOT_FOUND)

    # Update the recipe with the new data
    recipe.type = recipe_data.get('type')
    recipe.ingredients = recipe_data.get('ingredients')
    recipe.steps = recipe_data.get('steps')
    recipe.category_id = recipe_data.get('category_id')

    db.session.commit()

    return generate_response(data=recipe.to_dict(), message="Recipe edited successfully", status=HTTP_200_OK)

# Deleting a recipe

def delete_recipe(request, category_id, recipe_id):
    # Get user ID from token in request headers
    authorization_header = request.headers.get('Authorization')
    print('authorization_header',authorization_header)  
    token = request.headers.get('Authorization').split(' ')[1]
    decoded_token = TokenGenerator.decode_token(token)
    user_id = decoded_token.get('id')

    # Retrieve the recipe to be deleted
    recipe = Recipe.query.filter_by(id=recipe_id, category_id=category_id, user_id=user_id).first()
    if not recipe:
        return generate_response(message="Recipe not found", status=HTTP_404_NOT_FOUND)

    # Delete the recipe
    db.session.delete(recipe)
    db.session.commit()

    return generate_response(message="Recipe deleted", status=HTTP_200_OK)
