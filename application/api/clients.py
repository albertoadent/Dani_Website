from flask import Blueprint
from application.models import Client, db

clients = Blueprint("clients", __name__)


@clients.route("")
def get_clients():
    return [t.to_json() for t in Client.query.all()]


@clients.route("/<int:client_id>")
def get_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return {"errors": "Not Found"}, 404
    return client.to_json()
