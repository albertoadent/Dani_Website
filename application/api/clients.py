from flask import Blueprint, request
from .data_validation import validate, error_404, keys_to_snake
from application.models import Client, Location, db

clients = Blueprint("clients", __name__)

"""
GET ROUTES
"""


@clients.route("")
def get_clients():
    return [t.to_json() for t in Client.query.all()]


@clients.route("/<int:client_id>")
def get_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return {"errors": "Not Found"}, 404
    return client.to_json()


"""
POST ROUTES
"""

p = {"methods": ["POST"]}


@clients.route("", **p)
def post_client():
    data = request.get_json()
    res = validate(
        {
            "firstName": str,
            "lastName": str,
            "email": str,
            "phoneNumber": int,
            "address": str,
            "city": str,
            "state": str,
            "country": str,
            "preferredMethodOfCommunication": str,
        },
        data,
        ["preferredMethodOfCommunication"],
    )
    if res:
        return res

    location_data = {
        key: data[key] for key in data if key in ["address", "city", "state", "country"]
    }

    client_data = {
        key: data.get(key)
        for key in data
        if key not in ["address", "city", "state", "country"]
    }

    client = Client.query.filter_by(
        **keys_to_snake(
            {
                key: data.get(key)
                for key in data
                if key in ["firstName", "lastName", "email", "phoneNumber"]
            }
        )
    ).first()

    location = Location.query.filter_by(**location_data).first()
    if not location:
        location = Location(**location_data)
        db.session.add(location)
        db.session.commit()

    if not client:
        client = Client(**keys_to_snake(client_data), location=location)
        db.session.add(client)
        db.session.commit()
    return Client.query.get(int(client.id)).to_json()


p = {"methods": ["POST"]}


@clients.route("exists", **p)
def client_exists():
    data = request.get_json()
    res = validate(
        {
            "firstName": str,
            "lastName": str,
            "email": str,
            "phoneNumber": int,
        },
        data,
        ["firstName", "lastName"],
    )
    if res:
        return res

    client_data = {
        key: data.get(key)
        for key in data
        if key in ["firstName", "lastName", "email", "phoneNumber"]
    }

    client = Client.query.filter_by(**keys_to_snake(client_data)).first()
    print(client)
    if not client:
        return error_404(client)
    return client.to_json()


"""
PUT ROUTES
"""

pu = {"methods": ["PUT"]}


@clients.route("/<int:client_id>", **pu)
def put_client(client_id):
    data = request.get_json()
    res = validate(
        {
            "firstName": str,
            "lastName": str,
            "email": str,
            "phoneNumber": int,
            "address": str,
            "city": str,
            "state": str,
            "country": str,
            "preferredMethodOfCommunication": str,
        },
        data,
        ["preferredMethodOfCommunication"],
    )
    if res:
        return res

    location_data = {
        key: data[key] for key in data if key in ["address", "city", "state", "country"]
    }

    client_data = {
        key: data.get(key)
        for key in data
        if key not in ["address", "city", "state", "country"]
    }

    location = Location.query.filter_by(**location_data).first()
    if not location:
        location = Location(**location_data)
        db.session.add(location)
        db.session.commit()

    client = Client.query.get(client_id)
    if error_404(client):
        return error_404(client)

    client.first_name = client_data["firstName"]
    client.last_name = client_data["lastName"]
    client.email = client_data["email"]
    client.phone_number = client_data["phoneNumber"]
    client.preferred_method_of_communication = (
        client_data.get("preferredMethodOfCommunication")
        or client.preferred_method_of_communication
    )
    client.location_id = location.id

    db.session.commit()
    return Client.query.get(int(client.id)).to_json()


"""
DELETE ROUTES
"""

d = {"methods": ["DELETE"]}


@clients.route("/<int:client_id>", **d)
def delete_client(client_id):
    client = Client.query.get(client_id)

    if error_404(client):
        return error_404(client)

    db.session.delete(client)
    db.session.commit()

    return {"message": "deleted successfully"}
