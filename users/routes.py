from flask_restful import Api
from users.views import LoginApi, ForgotPassword, SignUpApi, ResetPassword, AllUsersApi, UserApi


def create_authentication_routes(api: Api):
    
    api.add_resource(SignUpApi, "/api/auth/register/")
    api.add_resource(AllUsersApi, "/api/auth/users/")
    api.add_resource(UserApi, "/api/auth/users/<int:user_id>/")
    api.add_resource(LoginApi, "/api/auth/login/")
    api.add_resource(ForgotPassword, "/api/auth/forgot-password/")
    api.add_resource(ResetPassword, "/api/auth/reset-password/<token>")