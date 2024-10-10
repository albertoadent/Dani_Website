from flask import Blueprint, request
from app.models import Admin, db
from app.forms.login_form import LoginForm
from app.forms.signup_form import SignUpForm
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_

User = Admin  # pyright: ignore

auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/")
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        return current_user.to_json()
    return {"errors": {"message": "Unauthorized"}}, 401


@auth_routes.route("/login", methods=["POST"])
def login():
    """
    Logs a user in
    """
    form = LoginForm()
    # Get the csrf_token from the request cookie and put it into the
    # form manually to validate_on_submit can be used
    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        # Add the user to the session, we are logged in!
        user = Admin.query.filter(
            or_(Admin.username == form.data["credential"], Admin.email == form.data["credential"])
        ).first()
        login_user(user)
        return user.to_json()

    return form.errors, 401


@auth_routes.route("/logout")
@login_required
def logout():
    """
    Logs a user out
    """
    logout_user()
    return {"message": "User logged out"}


@auth_routes.route("/signup", methods=["POST"])
def sign_up():
    """
    Creates a new user and logs them in
    """
    form = SignUpForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        user = Admin(
            email=form.data["email"],
            password=form.data["password"],
            first_name=form.data["first_name"],
            last_name=form.data["last_name"],
            bio=form.data["bio"],
        )
        db.session.add(user)
        db.session.commit()

        login_user(user)
        print(user.to_dict(), user.to_json())
        return user.to_json()

    return form.errors, 401


@auth_routes.route("/unauthorized")
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {"errors": {"message": "Unauthorized"}}, 401
