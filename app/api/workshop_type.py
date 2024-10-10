from flask import Blueprint, request
from app.models import WorkshopType, db
from .data_validation import validate, error_404

workshop_types = Blueprint("workshopTypes", __name__)

"""
GET ROUTES
"""


@workshop_types.route("")
def get_types():
    return [t.to_json() for t in WorkshopType.query.all()]


@workshop_types.route("/<int:workshop_id>")
def get_type(workshop_id):
    workshop_type = WorkshopType.query.get(workshop_id)
    if error_404(workshop_type):
        return error_404(workshop_type)
    return workshop_type.to_json()


"""
POST ROUTES
"""

p = {"methods": ["POST"]}


@workshop_types.route("", **p)
def post_type():
    data = request.get_json()
    res = validate(
        {"type": str, "description": str, "price": float, "timeFrame": float}, data
    )
    if res:
        return res

    w_type = WorkshopType(
        type=data["type"],
        description=data["description"],
        price=(data["price"]),
        time_frame=(data["timeFrame"]),
    )
    db.session.add(w_type)
    db.session.commit()
    return WorkshopType.query.get(int(w_type.id)).to_json()


"""
PUT ROUTES
"""

pu = {"methods": ["PUT"]}


@workshop_types.route("/<int:workshop_id>", **pu)
def put_type(workshop_id):
    data = request.get_json()

    try:
        res = validate(
            {"type": str, "description": str, "price": float, "timeFrame": float}, data
        )

        if res:
            return res

        w_type = WorkshopType.query.get(workshop_id)

        if error_404(w_type):
            return error_404(w_type)

        w_type.type = data["type"]
        w_type.description = data["description"]
        w_type.price = data["price"]
        w_type.time_frame = data["timeFrame"]
        db.session.commit()
        return WorkshopType.query.get(workshop_id).to_json()
    except ValueError:
        return {"message": "Bad Data", "errors": {}}, 400


"""
DELETE ROUTES
"""

d = {"methods": ["DELETE"]}


@workshop_types.route("/<int:workshop_id>", **d)
def delete_type(workshop_id):
    w_type = WorkshopType.query.get(workshop_id)

    if error_404(w_type):
        return error_404(w_type)

    db.session.delete(w_type)
    db.session.commit()

    return {"message": "deleted successfully"}
