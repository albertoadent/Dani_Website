from flask import Blueprint
from application.models import Workshop, db

workshops = Blueprint("workshops", __name__)


@workshops.route("")
def get_workshops():
    return [t.to_json() for t in Workshop.query.all()]


@workshops.route("/<int:workshop_id>")
def get_workshop(workshop_id):
    workshop_ = Workshop.query.get(workshop_id)
    if not workshop_:
        return {"errors": "Not Found"}, 404
    return workshop_.to_json()
