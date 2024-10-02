from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from application.models import Admin


def user_exists(form, field):
    # Checking if user exists
    email = field.data
    user = Admin.query.filter(Admin.email == email).first()
    if user:
        raise ValidationError('Email address is already in use.')


def username_exists(form, field):
    # Checking if username is already in use
    username = field.data
    user = Admin.query.filter(Admin.username == username).first()
    if user:
        raise ValidationError('Username is already in use.')


class SignUpForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email('Please enter a valid email'), user_exists])
    username = StringField('username', validators=[DataRequired(), username_exists])
    name = StringField('name', validators=[DataRequired('Name is required.')])
    password = StringField('password', validators=[DataRequired('Please enter a valid password.')])
