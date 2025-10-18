"""
forms.py

WTForms definitions used by the Flask application.

This module defines two Flask-WTF form classes used for user authentication:
- RegisterForm: used to create a new user account (name, username, password, confirm).
- LoginForm: used to log an existing user in (username, password).

Validators enforce minimal requirements such as presence, length limits, and password confirmation.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[Length(max=150)])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")
