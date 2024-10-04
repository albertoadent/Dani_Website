from datetime import datetime
from flask import Flask
from application.models import db, Content, Page, environment, SCHEMA
from sqlalchemy.sql import text


def seed_contents():

    Content3 = Content(
        page=Page.query.filter_by(name="Main").first(),
        header="Log In Here",
        sub_header="Sub Header",
        link_to="/login",
    )
    db.session.add(Content3)
    db.session.commit()

    Content1 = Content(
        page=Page.query.filter_by(name="Main").first(),
        header="Counseling Services",
        text="Feel free to contact me with any of your counseling concerns",
    )

    db.session.add(Content1)
    db.session.commit()

    Content2 = Content(
        page=Page.query.filter_by(name="Main").first(),
        header="Consultation services",
    )
    db.session.add(Content2)
    db.session.commit()
    
    Content4 = Content(
        page=Page.query.filter_by(name="Main").first(),
        header="Workshops",
        text="Check out the workshops that we offer",
        link_to="/workshops",
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
