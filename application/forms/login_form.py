from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError
from sqlalchemy import or_

User = {}


def user_exists(form, field):
    # Checking if user exists
    credential = field.data
    user = User.query.filter(
        or_(User.username == credential, User.email == credential)
    ).first()
    if not user:
        if "@" in credential:
            raise ValidationError("Email provided not found.")
        else:
            raise ValidationError("Username provided not found.")

def password_matches(form, field):
    # Checking if password matches
    password = field.data
    credential = form.data["credential"]
    user = User.query.filter(
        or_(User.username == credential, User.email == credential)
    ).first()
    if not user:
        raise ValidationError()
    if not user.check_password(password):
        raise ValidationError("Password was incorrect.")


class LoginForm(FlaskForm):
    credential = StringField("credential", validators=[DataRequired(), user_exists])
    password = StringField("password", validators=[DataRequired(), password_matches])
