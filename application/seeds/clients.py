from datetime import datetime
from flask import Flask
from application.models import db, Client, environment, SCHEMA
from sqlalchemy.sql import text


def seed_clients():
    concerned_parent = Client(
        first_name="Rudolph",
        last_name="Rednose",
        phone_number=1112345567,
        email="rudolph@therednose.com",
        preferred_method_of_communication="call",
        location_id=1
    )
    queer_kid = Client(
        first_name="Ace",
        last_name="Smith",
        phone_number=1112345568,
        email="iamqueer@queer.com",
        preferred_method_of_communication="text",
        location_id=2
    )
    teacher = Client(
        first_name="Amy",
        last_name="Winterhouse",
        phone_number=1113345567,
        email="teacher@school.org",
        preferred_method_of_communication="email",
        location_id=3
    )
    ceo = Client(
        first_name="Maya",
        last_name="Grier",
        phone_number=1112346567,
        email="maya@ceo.com",
        preferred_method_of_communication="email",
        location_id=4
    )

    db.session.add_all([concerned_parent,queer_kid,teacher,ceo])

    db.session.commit()


def undo_clients():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.clients RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM clients"))

    db.session.commit()
