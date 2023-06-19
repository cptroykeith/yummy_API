"""App entry point."""
"""Initialize Flask app."""
import os
from flask import Blueprint, Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flasgger import Swagger

import logging
logging.basicConfig(level=logging.DEBUG)

db = SQLAlchemy()
mail = Mail()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    # This is the configuration for the email server.
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_HOST_USER")
    app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_HOST_PASSWORD")
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True

    mail = Mail(app)

    app.config.from_object("config.Config")

    api = Api(app=app)

    from app.routes import create_authentication_routes

    create_authentication_routes(api=api)

    db.init_app(app)
    migrate = Migrate(app, db)
    mail.init_app(app)

    swagger = Swagger(
    app,
    template={
        "swagger": "2.0",
        "info": {
            "title": "Yummy_API",
            "description": "An API to keep track of food categories and recipes",
            "contact": {
                "name": "Roy William",
                "email": "katongole.roy100@gmail.com",
                "url": ""
            },
        },
        "version": "1.0.0",
        "basePath": "",
        "schemes": ["http", "https"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            }
        },
        "definitions": {
            "RecipesResponse": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "type": {"type": "string"},
                                "ingredients": {"type": "string"},
                                "steps": {"type": "string"},
                                "category_id": {"type": "integer"}
                            }
                        }
                    },
                    "message": {"type": "string"}
                }
            },
            "RecipeResponse": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "type": {"type": "string"},
                            "ingredients": {"type": "string"},
                            "steps": {"type": "string"},
                            "category_id": {"type": "integer"}
                        }
                    },
                    "message": {"type": "string"}
                }
            },
            "MessageResponse": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            }
        }
    }
)


    with app.app_context():
            db.create_all()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)