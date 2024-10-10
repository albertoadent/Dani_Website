from datetime import datetime
from flask import Flask
from app.models import db, WorkshopType, Workshop, Client, environment, SCHEMA
from sqlalchemy.sql import text


def seed_workshops():
    parent = Client.query.filter_by(first_name="Rudolph").first()
    kid = Client.query.filter_by(first_name="Ace").first()
    teacher = Client.query.filter_by(first_name="Amy").first()
    ceo = Client.query.filter_by(first_name="Maya").first()

    queerness = Workshop(
        type=WorkshopType.query.filter_by(type="Queerness 101").first(),
        start_date="2025-10-09 14:30:00",
        client=kid,
    )
    how_to_support = Workshop(
        type=WorkshopType.query.filter_by(
            type="How to support your LGBTQIA kid"
        ).first(),
        start_date="2025-11-01 14:30:00",
        client=parent,
    )

    sex_ed = Workshop(
        type=WorkshopType.query.filter_by(type="Sex-Ed").first(),
        start_date="2025-10-11 14:30:00",
        client=teacher,
    )

    leadership = Workshop(
        type=WorkshopType.query.filter_by(type="Being a Leader").first(),
        start_date="2025-10-10 14:30:00",
        client=ceo,
    )

    db.session.add_all([how_to_support, queerness, sex_ed, leadership])

    db.session.commit()


def undo_workshops():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.workshops RESTART IDENTITY CASCADE;"
        )
    else:
        db.session.execute(text("DELETE FROM workshops"))

    db.session.commit()
