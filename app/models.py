"""Data models."""
import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from . import db
from sqlalchemy.orm import relationship


# The User class is a data model for user accounts
class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)

    # Define a one-to-many relationship between User and Category
    categories = db.relationship("Category", backref="user", lazy=True)

    def __init__(self, **kwargs):
        
        self.username = kwargs.get("username")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")

    def __repr__(self):
        
        return "<User {}>".format(self.username)

    def hash_password(self):
        
        self.password = generate_password_hash(self.password).decode("utf8")

    def check_password(self, password):
        
        return check_password_hash(self.password, password)
    
class Category(db.Model):
    """Data model for categories."""

    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")

    def __repr__(self):
        return "<Category {}>".format(self.name)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "user_id": self.user_id,
        } 

class Recipe(db.Model):
    """Data model for recipes."""

    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), unique=True, nullable=False)
    ingredients = db.Column(db.String(500), nullable=False)
    steps = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = relationship("Category", backref="recipes")#A many-to-one relationship between recipe and category

    def __init__(self, **kwargs):
        self.type = kwargs.get("type")
        self.ingredients = kwargs.get("ingredients")
        self.steps = kwargs.get("steps")
        self.category_id = kwargs.get("category_id")

    def __repr__(self):
        return "<Recipe {}>".format(self.type)

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "ingredients": self.ingredients,
            "steps": self.steps,
            "user_id": self.user_id,
            "category_id": self.category_id,
        }
