from datetime import datetime
from flask import Flask
from app.models import db, Template, environment, SCHEMA
from sqlalchemy.sql import text


def seed_templates():
    main = Template(name="Main")
    workshops = Template(name="workshops")

    db.session.add_all([main, workshops])

    db.session.commit()


def undo_templates():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.templates RESTART IDENTITY CASCADE;"
        )
    else:
        db.session.execute(text("DELETE FROM templates"))

    db.session.commit()
