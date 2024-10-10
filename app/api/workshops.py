from flask import Blueprint, request
from flask_login import current_user, login_required
from app.models import Workshop, WorkshopType, Client, db
from datetime import datetime, timedelta
from .data_validation import validate, error_404

workshops = Blueprint("workshops", __name__)

"""
GET ROUTES
"""


@workshops.route("")
def get_workshops():
    return [t.to_json() for t in Workshop.query.all()]


@workshops.route("/<int:workshop_id>")
def get_workshop(workshop_id):
    workshop_ = Workshop.query.get(workshop_id)
    if not workshop_:
        return {"errors": "Not Found"}, 404
    return workshop_.to_json()


"""
POST ROUTES
"""

p = {"methods": ["POST"]}


@workshops.route("", **p)
def post_workshop():
    data = request.get_json()
    res = validate(
        {
            "workshopTypeId": int,
            "startDate": datetime,
            "clientId": int,
        },
        data,
    )
    if res:
        return res
    client = Client.query.get(data["clientId"])
    if error_404(client):
        return error_404(client)
    w_type = Workshop(
        workshop_type_id=data["workshopTypeId"],
        start_date=data["startDate"],
        client_id=client.id
    )
    interfere_workshops = Workshop.query.filter(
        Workshop.start_date < w_type.end_date, Workshop.end_date > w_type.start_date
    ).first()
    if interfere_workshops:
        return {
            "message": "Bad Data",
            "errors": {
                "startDate": "Your start date conflicts with an existing workshop"
            },
        }, 400
    db.session.add(w_type)
    db.session.commit()
    return Workshop.query.get(int(w_type.id)).to_json()


"""
PUT ROUTES
"""

pu = {"methods": ["PUT"]}


@workshops.route("/<int:workshop_id>", **pu)
def put_workshop(workshop_id):
    data = request.get_json()
    res = validate(
        {
            "startDate": datetime,
        },
        data,
    )
    if res:
        return res
    workshop = Workshop.query.get(workshop_id)
    if error_404(workshop):
        return error_404(workshop)

    end_date = data["startDate"] + timedelta(minutes=(workshop.type.time_frame * 60))

    print(end_date)
    print(data["startDate"])

    interfere_workshops = Workshop.query.filter(
        Workshop.start_date < end_date,
        Workshop.end_date > data["startDate"],
        Workshop.id != workshop_id,
    ).first()
    if interfere_workshops:
        return {
            "message": "Bad Data",
            "errors": {
                "startDate": "Your start date conflicts with an existing workshop",
                "conflictId": interfere_workshops.id,
            },
        }, 400
    workshop.start_date = data["startDate"]
    workshop.end_date = end_date
    db.session.commit()
    return Workshop.query.get(workshop_id).to_json()


"""
DELETE ROUTES
"""

d = {"methods": ["DELETE"]}


@workshops.route("/<int:workshop_id>", **d)
def delete_type(workshop_id):

    workshop = Workshop.query.get(workshop_id)


    if not workshop:
        return error_404(workshop)

    db.session.delete(workshop)
    db.session.commit()

    return {"message": "deleted successfully"}
