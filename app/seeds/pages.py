from datetime import datetime
from flask import Flask
from app.models import db, Page, environment, SCHEMA
from sqlalchemy.sql import text


def seed_pages():
    page1 = Page(name="Main", is_public=True)
    page2 = Page(name="Secondary")
    page3 = Page(name="Alt Main")
    page4 = Page(name="Alt Secondary")

    db.session.add_all([page1, page2, page3, page4])

    db.session.commit()


def undo_pages():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.pages RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM pages"))

    db.session.commit()
