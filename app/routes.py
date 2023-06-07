from flask_restful import Api
from .views import (DeleteRecipeApi, EditRecipeApi, GetRecipeByCategoryApi, GetRecipesByCategoryApi, LoginApi, ForgotPassword, SignUpApi,
ResetPassword, AllUsersApi, UserApi, GetUserApi, CreateCategoryApi,
GetUserCategoriesApi, GetCategoryApi, EditCategoryApi, DeleteCategoryApi,
CreateRecipeApi)


def create_authentication_routes(api: Api):
    
    api.add_resource(SignUpApi, "/api/auth/register/")
    api.add_resource(LoginApi, "/api/auth/login/")
    api.add_resource(AllUsersApi, "/api/auth/users/")
    api.add_resource(UserApi, "/api/auth/users/<int:user_id>/")
    api.add_resource(GetUserApi, "/api/auth/users/<int:user_id>/")
    api.add_resource(ForgotPassword, "/api/auth/forgot-password/")
    api.add_resource(ResetPassword, "/api/auth/reset-password/<token>")
    api.add_resource(CreateCategoryApi, "/api/categories/create/")
    api.add_resource(GetUserCategoriesApi, "/api/categories/get-categories/")
    api.add_resource(GetCategoryApi, "/api/categories/<int:category_id>/")
    api.add_resource(EditCategoryApi, "/api/categories/<int:category_id>/edit/")
    api.add_resource(DeleteCategoryApi, "/api/categories/<int:category_id>/delete/")
    api.add_resource(CreateRecipeApi, "/api/recipes/create/")
    api.add_resource(GetRecipesByCategoryApi, "/api/categories/<int:category_id>/recipes/")
    api.add_resource(GetRecipeByCategoryApi, "/api/categories/<int:category_id>/recipes/<int:recipe_id>/")
    api.add_resource(EditRecipeApi, "/api/categories/<int:category_id>/recipes/<int:recipe_id>/")
    api.add_resource(DeleteRecipeApi, "/api/categories/<int:category_id>/recipes/<int:recipe_id>/")
