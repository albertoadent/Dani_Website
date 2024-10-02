from datetime import datetime
from flask import Flask
from application.models import db, Admin, environment, SCHEMA
from sqlalchemy.sql import text


def seed_admins():
    alberto = Admin(
        username="albertoadent",
        email="albertoadent@gmail.com",
        name="Alberto Dent",
        password="password",
    )
    dani = Admin(
        username="danialberto",
        email="herreradentd95@outlook.com",
        name="Dani Alberto",
        password="password",
    )

    db.session.add_all([dani, alberto])

    db.session.commit()


def undo_admins():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.Admins RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM Admins"))

    db.session.commit()
