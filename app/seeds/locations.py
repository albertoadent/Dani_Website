from datetime import datetime
from flask import Flask
from app.models import db, Location, environment, SCHEMA
from sqlalchemy.sql import text


def seed_locations():
    location1 = Location(
        address="123 Market St", city="Los Angeles", state="CA", country="United States"
    )
    location2 = Location(
        address="1234 Day Rd", city="Atlanta", state="GA", country="United States"
    )
    location3 = Location(
        address="543 WoodStock Dr", city="Austin", state="TX", country="United States"
    )
    location4 = Location(
        address="555 River Rd",
        city="Salt Lake City",
        state="UT",
        country="United States",
    )

    db.session.add_all([location1, location2, location3, location4])

    db.session.commit()


def undo_locations():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.locations RESTART IDENTITY CASCADE;"
        )
    else:
        db.session.execute(text("DELETE FROM locations"))

    db.session.commit()
