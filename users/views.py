from flask import Response
from flask_restful import Resource
from flask import request, make_response
from users.service import create_user, reset_password_email_send, login_user, reset_password, get_all_users, delete_user ,get_user_by_id


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
