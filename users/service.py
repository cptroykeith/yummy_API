import json
import jwt
import datetime
from server import db
from os import environ
from users.helper import send_forgot_password_email
from users.models import User, Category
from flask_bcrypt import generate_password_hash
from utils.common import generate_response, TokenGenerator
from users.validation import (
    CreateLoginInputSchema,
    CreateResetPasswordEmailSendInputSchema,
    CreateSignupInputSchema, ResetPasswordInputSchema, CreateCategoryInputSchema,
)
from utils.http_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED


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
            message="Username already exist", status=HTTP_400_BAD_REQUEST
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

def get_all_users(request):
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {}
        user_data["id"] = user.id
        user_data["username"] = user.username
        user_data["email"] = user.email
        user_list.append(user_data)
    return generate_response(data=user_list, message="All users retrieved", status=HTTP_200_OK)

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
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
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

    # Get user ID from token in request headers
    token = request.headers.get('Authorization')
    decoded_token = TokenGenerator.decode_token(token)
    user_id = decoded_token.get('id')
    
    # Create new category with user ID
    new_category = Category(**category_data)
    new_category.user_id = user_id
    db.session.add(new_category)
    db.session.commit()

    return generate_response(data=category_data, message="Category created", status=HTTP_201_CREATED)

def get_user_categories(request):
    # Get user ID from token in request headers
    token = request.headers.get('Authorization')
    decoded_token = TokenGenerator.decode_token(token)
    user_id = decoded_token.get('id')

    # Get all categories for user ID
    categories = Category.query.filter_by(user_id=user_id).all()

    # Serialize categories using CategorySchema
    category_schema = CreateCategoryInputSchema(many=True)
    categories_data = category_schema.dump(categories)

    return generate_response(data=categories_data, message="Categories retrieved", status=HTTP_200_OK)
