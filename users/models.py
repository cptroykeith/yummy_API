"""Data models."""
import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from server import db


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
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.description = kwargs.get("description")

    def __repr__(self):
        return "<Category {}>".format(self.name)