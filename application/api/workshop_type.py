from flask import Blueprint
from application.models import WorkshopType, db

workshop_types = Blueprint("workshopTypes", __name__)


@workshop_types.route("")
def get_types():
    return [t.to_json() for t in WorkshopType.query.all()]


@workshop_types.route("/<int:workshop_id>")
def get_type(workshop_id):
    workshop_type = WorkshopType.query.get(workshop_id)
    if not workshop_type:
        return {"errors": "Not Found"}, 404
    return workshop_type.to_json()
