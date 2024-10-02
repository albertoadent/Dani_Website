from datetime import datetime
from flask import Flask
from application.models import db, Template, environment, SCHEMA
from sqlalchemy.sql import text


def seed_templates():
    main = Template(name="Main")
    secondary = Template(name="Secondary")
    alt_main = Template(name="Alt Main")
    alt_secondary = Template(name="Alt Secondary")

    db.session.add_all([main, secondary, alt_main, alt_secondary])

    db.session.commit()


def undo_templates():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.Templates RESTART IDENTITY CASCADE;"
        )
    else:
        db.session.execute(text("DELETE FROM Templates"))

    db.session.commit()
