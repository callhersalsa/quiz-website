"""
models.py

SQLAlchemy ORM models for the Flask application.

This module defines the User model which represents a registered user in the
application. Fields include identification, credentials (password stored as
a hashed value), a game score, and timestamps. Utility methods handle password
hashing and verification using Werkzeug security helpers.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Hash and store password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Return True if password matches hash."""
        return check_password_hash(self.password_hash, password)
