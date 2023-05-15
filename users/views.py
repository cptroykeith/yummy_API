from flask import Response
from flask_restful import Resource
from flask import request, make_response
from users.service import (create_user, edit_recipe, get_recipe_by_id, get_recipes_by_category, reset_password_email_send, 
login_user, reset_password, get_all_users, delete_user ,get_user_by_id,
create_category, get_user_categories, get_category, edit_category,
delete_category, create_recipe )
from utils.common import TokenGenerator

class SignUpApi(Resource):
    @staticmethod
    def post() -> Response:
   
        input_data = request.get_json()
        response, status = create_user(request, input_data)
        return make_response(response, status)


class LoginApi(Resource):
    @staticmethod
    def post() -> Response:
        
        input_data = request.get_json()
        response, status = login_user(request, input_data)
        return make_response(response, status)
    
class AllUsersApi(Resource):
    @staticmethod
    def get() -> Response:
        
        response, status = get_all_users(request)
        return make_response(response, status)
    
class GetUserApi(Resource):
    @staticmethod
    def get(user_id) -> Response:
        response, status = get_user_by_id(request, user_id)
        return make_response(response, status)
    
class UserApi(Resource):
    @staticmethod
    def delete(user_id: int) -> Response:
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
         input_data = request.get_json()
         response, status = create_category(request, input_data)
         return make_response(response, status)
    
class GetUserCategoriesApi(Resource):
    @staticmethod
    def get() -> Response:
        response, status = get_user_categories(request)
        return make_response(response, status)
    
class GetCategoryApi(Resource):
    @staticmethod
    def get(category_id: int) -> Response:
        response, status = get_category(request, category_id)
        return make_response(response, status)
    
class EditCategoryApi(Resource):
    def put(self, category_id: int) -> Response:
        category_data = request.get_json()
        response, status = edit_category(request, category_id, category_data)
        return response, status
    
class DeleteCategoryApi(Resource):
    @staticmethod
    def delete(category_id: int) -> Response:
        response, status = delete_category(request, category_id)
        return make_response(response, status)

class CreateRecipeApi(Resource):
    @staticmethod
    def post() -> Response:
        recipe_data = request.get_json()
        response, status = create_recipe(request, recipe_data)
        return make_response(response, status)
    
class GetRecipesByCategoryApi(Resource):
    @staticmethod
    def get(category_id: int) -> Response:
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
