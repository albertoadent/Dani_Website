from datetime import datetime
from flask import Flask
from application.models import db, WorkshopType, environment, SCHEMA
from sqlalchemy.sql import text


def seed_workshop_types():
    queerness = WorkshopType(
        type="Queerness 101",
        description="An introduction to what it means to be queer. We will explore the following prompts: Am I queer? How can I be an ally to the queer community?",
        price=300.00,
        time_frame=1.5,
    )
    how_to_support = WorkshopType(
        type="How to support your LGBTQIA kid",
        description="A Q&A session where I answer the difficult questions surrounding supporting your LGBTQIA kid. The first step for any parent that doesn't know how to deal with a challenging situation and wants to be there for their child",
        price=250.00,
        time_frame=1.0,
    )

    sex_ed = WorkshopType(
        type="Sex-Ed",
        description="A Sex-Ed course that give a comprehensive walkthrough of what sex is and how to engage with it in a healthy way that doesn't alienate people who aren't cis gender and/or straight",
        price=500.00,
        time_frame=1.0,
    )

    leadership = WorkshopType(
        type="Being a Leader",
        description="How to be a leader for your community when in positions of influence: How to employ Social Justice, equity based practices, and positive working environments",
        price=1000.00,
        time_frame=1.5,
    )

    db.session.add_all([how_to_support, queerness, sex_ed, leadership])

    db.session.commit()


def undo_workshop_types():
    if environment == "production":
        db.session.execute(
            f"TRUNCATE table {SCHEMA}.WorkshopTypes RESTART IDENTITY CASCADE;"
        )
    else:
        db.session.execute(text("DELETE FROM WorkshopTypes"))

    db.session.commit()
