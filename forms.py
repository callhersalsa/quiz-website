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
    name = StringField(
        "Full Name",
        validators=[DataRequired(message="✖ Full name is required."), Length(max=150)]
    )
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="✖ Username is required."),
            Length(min=3, max=80, message="✖ Username must be between 3 and 80 characters.")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="✖ Password is required."),
            Length(min=6, message="✖ Password must be at least 6 characters long.")
        ]
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="✖ Please confirm your password."),
            EqualTo('password', message='✖ Passwords must match.')
        ]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(message="✖ Username is required."), Length(min=3, max=80)]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="✖ Password is required.")]
    )
    submit = SubmitField("Login")
