from flask import Response, jsonify
from flask_restful import Resource
from flask import request, make_response
from app.service import (create_user, delete_recipe, edit_recipe, get_recipe_by_id, get_recipes_by_category, reset_password_email_send, 
login_user, reset_password, get_all_users, delete_user ,get_user_by_id,
create_category, get_user_categories, get_category, edit_category,
delete_category, create_recipe )
from utils.common import TokenGenerator
from utils.common import generate_response


class SignUpApi(Resource):
    @staticmethod
    def post() -> Response:
        """
User Signup

Endpoint for registering a new user with parameters: username, email, and password.

---
tags:
  - Authentication
parameters:
  - in: body
    name: body
    required: true
    description: JSON object containing user registration details
    schema:
      type: object
      properties:
        username:
          type: string
        email:
          type: string
        password:
          type: string
      example:
        {
          "username": "roy",
          "email": "roy@email.com",
          "password": "********"
        }
responses:
  201:
    description: User Created
  409:
    description: Username already exists
  400:
    description: Email  already taken
"""

   
        input_data = request.get_json()
        response, status = create_user(request, input_data)
        return make_response(response, status)


class LoginApi(Resource):
    @staticmethod
    def post() -> Response:
        """
    User Login Endpoint
    
    This endpoint is used to authenticate a user by their email and password.
    
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: The email of the user.
            password:
              type: string
              description: The password of the user.
    responses:
      201:
        description: User login successful.
        schema:
          type: object
          properties:
            token:
              type: string
              description: The JWT token for the authenticated user.
      400:
        description: Invalid email or password.
        schema:
          type: object
          properties:
            message:
              type: string
              description: Error message indicating the reason for the failure.
    """
        
        input_data = request.get_json()
        response, status = login_user(request, input_data)
        return make_response(response, status)
    
class AllUsersApi(Resource):
    @staticmethod
    def get() -> Response:
        """
        Get All Users Endpoint

        This endpoint retrieves all users from the database.

        ---
        tags:
          - Users
        responses:
          200:
            description: All users retrieved successfully.
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: The ID of the user.
                      username:
                        type: string
                        description: The username of the user.
                      email:
                        type: string
                        description: The email of the user.
                message:
                  type: string
                  description: Success message.
        """
        response, status = get_all_users()
        return make_response(response, status)

    
class GetUserApi(Resource):
    @staticmethod
    def get(user_id) -> Response:
        """
        Get User by ID Endpoint

        This endpoint retrieves a user from the database based on the provided user ID.

        ---
        tags:
          - Users
        parameters:
          - in: path
            name: user_id
            type: integer
            required: true
            description: The ID of the user to retrieve.
        responses:
          200:
            description: User retrieved successfully.
            schema:
              type: object
              properties:
                data:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: The ID of the user.
                    username:
                      type: string
                      description: The username of the user.
                    email:
                      type: string
                      description: The email of the user.
                message:
                  type: string
                  description: Success message.
          404:
            description: User not found.
        """
        response, status = get_user_by_id(request, user_id)
        return make_response(response, status)

    
class UserApi(Resource):
    @staticmethod
    def delete(user_id: int) -> Response:
        """
        Delete User Endpoint

        This endpoint deletes a user from the database based on the provided user ID.

        ---
        tags:
          - Users
        parameters:
          - in: path
            name: user_id
            type: integer
            required: true
            description: The ID of the user to delete.
        responses:
          200:
            description: User deleted successfully.
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Success message.
          404:
            description: User not found.
        """
        response, status = delete_user(request, user_id)
        return make_response(response, status)



class ForgotPassword(Resource):
    @staticmethod
    def post() -> Response:
      
        input_data = request.get_json()
        response, status = reset_password_email_send(request, input_data)
        return make_response(response, status)


class ResetPassword(Resource):
    @staticmethod
    def post(token) -> Response:
       
        input_data = request.get_json()
        response, status = reset_password(request, input_data, token)
        return make_response(response, status)
    
class CreateCategoryApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        Create Category Endpoint

        This endpoint creates a new category in the database based on the provided category data.
        The category is associated with the user identified by the authorization token present in the request headers.

        ---
        tags:
          - Categories
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: The name of the category.
                description:
                  type: string
                  description: The description of the category.
        security:
          - Bearer: []
        responses:
          201:
            description: Category created successfully.
            schema:
              type: object
              properties:
                data:
                  type: object
                  properties:
                    name:
                      type: string
                      description: The name of the category.
                    description:
                      type: string
                      description: The description of the category.
                message:
                  type: string
                  description: Success message.
          400:
            description: Invalid input data or category already exists.
          401:
            description: Unauthorized access, missing or invalid authorization token.
        """
        input_data = request.get_json()
        response, status = create_category(request, input_data)
        return make_response(response, status)


class GetUserCategoriesApi(Resource):
    @staticmethod
    def get() -> Response:
        """
        Get User Categories Endpoint

        This endpoint retrieves all categories associated with the user identified by the authorization token
        present in the request headers.

        ---
        tags:
          - Categories
        security:
          - Bearer: []
        responses:
          200:
            description: Categories retrieved successfully.
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      name:
                        type: string
                        description: The name of the category.
                      description:
                        type: string
                        description: The description of the category.
                message:
                  type: string
                  description: Success message.
          401:
            description: Unauthorized access, missing or invalid authorization token.
        """
        response, status = get_user_categories(request)
        return make_response(response, status)
    
class GetCategoryApi(Resource):
    @staticmethod
    def get(category_id: int) -> Response:
        """
        Get Category Endpoint

        This endpoint retrieves the category with the specified ID associated with the user identified by the
        authorization token present in the request headers.

        ---
        tags:
          - Categories
        parameters:
          - in: path
            name: category_id
            type: integer
            required: true
            description: The ID of the category to retrieve.
        security:
          - Bearer: []
        responses:
          200:
            description: Category retrieved successfully.
            schema:
              type: object
              properties:
                data:
                  type: object
                  properties:
                    name:
                      type: string
                      description: The name of the category.
                    description:
                      type: string
                      description: The description of the category.
                message:
                  type: string
                  description: Success message.
          401:
            description: Unauthorized access, missing or invalid authorization token.
          404:
            description: Category not found.
        """
        response, status = get_category(request, category_id)
        return make_response(response, status)

    
class EditCategoryApi(Resource):
    def put(self, category_id: int) -> Response:
        """
        Edit Category Endpoint

        This endpoint updates the category with the specified ID for the user identified by the authorization token
        present in the request headers.

        ---
        tags:
          - Categories
        parameters:
          - in: path
            name: category_id
            type: integer
            required: true
            description: The ID of the category to edit.
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: The updated name of the category.
                description:
                  type: string
                  description: The updated description of the category.
        security:
          - Bearer: []
        responses:
          200:
            description: Category updated successfully.
            schema:
              type: object
              properties:
                data:
                  type: object
                  properties:
                    name:
                      type: string
                      description: The updated name of the category.
                    description:
                      type: string
                      description: The updated description of the category.
                message:
                  type: string
                  description: Success message.
          401:
            description: Unauthorized access, missing or invalid authorization token.
          404:
            description: Category not found.
        """
        category_data = request.get_json()
        response, status = edit_category(request, category_id, category_data)
        return response, status

class DeleteCategoryApi(Resource):
    def delete(self, category_id: int) -> Response:
        """
        Delete Category Endpoint

        This endpoint deletes the category with the specified ID for the user identified by the authorization token
        present in the request headers. It also deletes all the recipes associated with the category and user.

        ---
        tags:
          - Categories
        parameters:
          - in: path
            name: category_id
            type: integer
            required: true
            description: The ID of the category to delete.
          - in: query
            name: confirmation
            type: string
            required: false
            description: The confirmation parameter ('yes' or 'no') to confirm or cancel deletion.
        security:
          - Bearer: []
        responses:
          200:
            description: Category deleted successfully.
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: Success message.
          400:
            description: Invalid confirmation parameter or missing confirmation parameter.
          401:
            description: Unauthorized access, missing or invalid authorization token.
          404:
            description: Category not found.
        """
        response, status = delete_category(request, category_id)
        return make_response(response, status)


class CreateRecipeApi(Resource):
    @staticmethod
    def post() -> Response:
        """
        Create Recipe Endpoint

        This endpoint creates a new recipe in the database based on the provided recipe data.
        The recipe is associated with the user identified by the authorization token present in the request headers.

        ---
        tags:
          - Recipes
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                type:
                  type: string
                  description: The type of the recipe.
                ingredients:
                  type: string
                  description: The list of ingredients required for the recipe.
                steps:
                  type: string
                  description: The steps or instructions for preparing the recipe.
                category_id:
                  type: integer
                  description: The ID of the category to which the recipe belongs.
              required:
                - type
                - ingredients
                - steps
                - category_id
        security:
          - Bearer: []
        responses:
          201:
            description: Recipe created successfully.
            schema:
              $ref: '#/definitions/RecipeResponse'
          400:
            description: Invalid input data or recipe already exists.
          401:
            description: Unauthorized access, missing or invalid authorization token.
        """
        recipe_data = request.get_json()
        response, status = create_recipe(request, recipe_data)
        return make_response(response, status)
    
class GetRecipesByCategoryApi(Resource):
    @staticmethod
    def get(category_id: int) -> Response:
        """
        Get Recipes by Category Endpoint

        This endpoint retrieves all recipes belonging to a specific category for the authenticated user.

        ---
        tags:
          - Recipes
        parameters:
          - in: path
            name: category_id
            required: true
            description: The ID of the category to filter recipes.
            schema:
              type: integer
        security:
          - Bearer: []
        responses:
          200:
            description: Recipes retrieved successfully.
            schema:
              $ref: '#/definitions/RecipesResponse'
          404:
            description: No recipes found for the given user and category.
          401:
            description: Unauthorized access, missing or invalid authorization token.
        """
        # Get user ID from token in request headers
        token = request.headers.get('Authorization')
        decoded_token = TokenGenerator.decode_token(token)
        user_id = decoded_token.get('id')

        # Retrieve recipes for the given user and category
        response = get_recipes_by_category(user_id, category_id)
        return make_response(response)

    
class GetRecipeByCategoryApi(Resource):
    @staticmethod
    def get(category_id: int, recipe_id: int) -> Response:
        """
        Get Recipe by Category and Recipe ID

        This endpoint retrieves a specific recipe for the given user, category, and recipe ID.
        The user is identified by the authorization token present in the request headers.

        ---
        tags:
          - Recipes
        parameters:
          - in: path
            name: category_id
            required: true
            type: integer
            description: The ID of the category.
          - in: path
            name: recipe_id
            required: true
            type: integer
            description: The ID of the recipe.
        security:
          - Bearer: []
        responses:
          200:
            description: Recipe retrieved successfully.
            schema:
              $ref: '#/definitions/RecipeResponse'
          404:
            description: Recipe not found.
        """
        # Get user ID from token in request headers
        token = request.headers.get('Authorization')
        decoded_token = TokenGenerator.decode_token(token)
        user_id = decoded_token.get('id')

        # Retrieve the recipe for the given user, category, and recipe ID
        response = get_recipe_by_id(user_id, category_id, recipe_id)
        return make_response(response)


class EditRecipeApi(Resource):
    @staticmethod
    def put(category_id: int, recipe_id: int) -> Response:
        recipe_data = request.get_json()
        response, status = edit_recipe(request, category_id, recipe_id, recipe_data)
        return make_response(response, status)
    
class DeleteRecipeApi(Resource):
    @staticmethod
    def delete(category_id: int, recipe_id: int) -> Response:
        # Get user ID from token in request headers
        token = request.headers.get('Authorization')
        decoded_token = TokenGenerator.decode_token(token)
        user_id = decoded_token.get('id')

        # Delete the recipe for the given user and category
        response = delete_recipe(request, category_id, recipe_id)
        return make_response(response)
