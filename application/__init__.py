import os
from flask import Flask, request, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import generate_csrf
from flask_login import LoginManager
from .models import db, Admin
from .seeds import seed_commands
from .config import Config

User = Admin
application = Flask(__name__, static_folder="../react-vite/dist", static_url_path="/")

# Setup login manager
login = LoginManager(application)
login.login_view = "auth.unauthorized"


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Tell flask about our seed commands
application.cli.add_command(seed_commands)

application.config.from_object(Config)

db.init_application(application)
Migrate(application, db)

# Application Security
CORS(application)


@application.before_request
def https_redirect():
    if os.environ.get("FLASK_ENV") == "production":
        if request.headers.get("X-Forwarded-Proto") == "http":
            url = request.url.replace("http://", "https://", 1)
            code = 301
            return redirect(url, code=code)


@application.after_request
def inject_csrf_token(response):
    response.set_cookie(
        "csrf_token",
        generate_csrf(),
        secure=True if os.environ.get("FLASK_ENV") == "production" else False,
        samesite="Strict" if os.environ.get("FLASK_ENV") == "production" else None,
        httponly=True,
    )
    return response


@application.route("/api/docs")
def api_help():
    """
    Returns all API routes and their doc strings
    """
    acceptable_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    route_list = {
        rule.rule: [
            [method for method in rule.methods if method in acceptable_methods],
            application.view_functions[rule.endpoint].__doc__,
        ]
        for rule in application.url_map.iter_rules()
        if rule.endpoint != "static"
    }
    return route_list


@application.route("/", defaults={"path": ""})
@application.route("/<path:path>")
def react_root(path):
    """
    This route will direct to the public directory in our
    react builds in the production environment for favicon
    or index.html requests
    """
    if path == "favicon.ico":
        return application.send_from_directory("public", "favicon.ico")
    return application.send_static_file("index.html")


@application.errorhandler(404)
def not_found(e):
    return application.send_static_file("index.html")
