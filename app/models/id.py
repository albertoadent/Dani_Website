from .db import db

class ID:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
