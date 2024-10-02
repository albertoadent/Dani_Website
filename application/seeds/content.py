from datetime import datetime
from flask import Flask
from application.models import db, Content, Page, environment, SCHEMA
from sqlalchemy.sql import text


def seed_contents():
    Content1 = Content(
        page=Page.query.filter_by(name="Main").first(),
        header="Seed Data from Main",
        sub_header="Sub Header",
        text="Here is some text that is for the description of this content",
    )

    db.session.add(Content1)
    db.session.commit()

    Content2 = Content(
        page=Page.query.filter_by(name="Main").first(),
        header="Seed Data 2 from Main",
        image_url="https://images.squarespace-cdn.com/content/v1/5f133f9f1f4b2a1a167b24e5/8f9680c1-9397-46cb-9432-e3e6f8506dc3/DALL%C2%B7E+2023-11-23+%7C+Teen+Therapist+%7C+Kansas+City+%7C+Blue+Springs+%7C+Lee%27s+Summit+%7C+Liberty+%7C+Independence?format=2500w",
    )
    db.session.add(Content2)
    db.session.commit()
    Content3 = Content(
        page=Page.query.filter_by(name="Main").first(),
        header="Seed Data 3 from Main",
        sub_header="Sub Header",
    )
    db.session.add(Content3)
    db.session.commit()
    Content4 = Content(
        page=Page.query.filter_by(name="Main").first(),
        header="Seed Data 4 from Main",
        text="Here is some text that is for the description of this content",
    )

    db.session.add(Content4)
    db.session.commit()


def undo_contents():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.Contents RESTART IDENTITY CASCADE;"
        )
    else:
        db.session.execute(text("DELETE FROM Contents"))

    db.session.commit()
