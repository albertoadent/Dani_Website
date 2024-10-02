from .jsonable import JSONable
from flask_login import UserMixin
from .timestamps import Timestamps
from .db import db, add_prefix_for_prod
from .id import ID
from werkzeug.security import generate_password_hash, check_password_hash


class CustomModel(db.Model, Timestamps, ID, JSONable):
    pass


class CustomUserModel(db.Model, UserMixin, Timestamps, ID, JSONable):
    pass


class CustomModelWithoutId(db.Model, Timestamps, JSONable):
    pass


"""
The website will only support logins for those that can edit the website
"""


class Admin(CustomUserModel):
    username = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


"""
The Website will mainly offer workshops that can be scheduled
"""


class WorkshopType(CustomModel):
    type = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    timeFrame = db.Column(db.Float, nullable=False)

    workshops = db.relationship("Workshop", back_populates="type")


class Workshop(CustomModel):
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    workshop_type_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("WorkshopTypes.id"))
    )

    type = db.relationship("WorkshopType", back_populates="workshops")

    @property
    def start(self):
        return self.get_timestamp_breakdown("start_date")

    @property
    def end(self):
        return self.get_timestamp_breakdown("end_date")


"""
The Following Models are all used to store the content on each page in the backend
The templates table will only be updated when a new template component is created on the frontend
The name of the Template will be the same as the name of the component on the frontend
"""


class Template(CustomModel):
    name = db.Column(db.String, nullable=False)


class Page(CustomModel):
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String, nullable=False)
    template_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("Templates.id"))
    )

    template = db.relationship("Template")
    content = db.relationship("Content", back_populates="page")


def gen_content_index(page_id):
    page = Page.query.get(int(page_id))
    if page is None:
        raise ValueError(f"Page with id {page_id} does not exist.")
    return f"{len(page.content)}_{page_id}"


class Content(CustomModelWithoutId):
    header = db.Column(db.String, nullable=True)
    sub_header = db.Column(db.String, nullable=True)
    text = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    page_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod("Pages.id")))

    page = db.relationship("Page", back_populates="content")

    def __init__(self, page_id, *args, **kwargs):
        self.id = gen_content_index(page_id=page_id)
        super().__init__(*args, **kwargs)


class Affirmations(CustomModel):
    affirmation = db.Column(db.String, nullable=False)
