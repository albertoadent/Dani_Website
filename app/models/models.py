from .jsonable import JSONable
from flask_login import UserMixin
from .timestamps import Timestamps
from .prod_ready import PROD
from .db import db, add_prefix_for_prod
from .id import ID
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

Model = db.Model


CustomModel = (Model, Timestamps, JSONable, PROD)
CustomUserModel = (Model, UserMixin, Timestamps, JSONable, PROD)
CustomModelWithoutId = (Timestamps, JSONable, PROD)


"""
The website will only support logins for those that can edit the website
"""


class Admin(*CustomUserModel):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
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


class WorkshopType(*CustomModel):
    __tablename__ = "workshop_types"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    time_frame = db.Column(db.Float, nullable=False)

    workshops = db.relationship("Workshop", back_populates="type")


class Location(*CustomModel):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)


class Workshop(*CustomModel):
    __tablename__ = "workshops"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    workshop_type_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod("workshop_types.id")),
        nullable=False,
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("locations.id")), nullable=False
    )
    client_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("clients.id")), nullable=False
    )

    location = db.relationship("Location")
    client = db.relationship("Client", back_populates="workshops")
    type = db.relationship("WorkshopType", back_populates="workshops")

    @property
    def start(self):
        return self.get_timestamp_breakdown("start_date")

    @property
    def end(self):
        return self.get_timestamp_breakdown("end_date")

    def __init__(
        self,
        type=None,
        start_date=None,
        workshop_type_id=None,
        client=None,
        client_id=None,
        location_id=None,
        *args,
        **kwargs,
    ):
        duration = 0.0
        if type:
            self.workshop_type_id = type.id
            duration = type.time_frame
        elif workshop_type_id:
            type = WorkshopType.query.get(int(workshop_type_id))
            self.workshop_type_id = workshop_type_id
            duration = type.time_frame

        seconds = duration * 60 * 60

        if isinstance(start_date, datetime):
            end_date = start_date + timedelta(seconds=seconds)
            self.start_date = start_date
        elif isinstance(start_date, str):
            end_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S") + timedelta(
                seconds=seconds
            )
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        else:
            raise ValueError("start_date must be a datetime or a string")

        self.end_date = end_date

        if client:
            self.client_id = client.id
            self.location_id = client.location_id
            print("\n\n\n\n", "LOCATION ID:", client.location_id, "\n\n\n\n")
        elif client_id:
            client = Client.query.get(int(client_id))
            self.client_id = client_id
            print("\n\n\n\n", "LOCATION ID:", client.location_id, "\n\n\n\n")
            self.location_id = client.location_id

        if location_id:
            self.location_id = location_id

        super().__init__(*args, **kwargs)


"""
The Following Models are all used to store the content on each page in the backend
The templates table will only be updated when a new template component is created on the frontend
The name of the Template will be the same as the name of the component on the frontend
"""


class Template(*CustomModel):
    __tablename__ = "templates"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String, nullable=False)

    pages = db.relationship("Page", back_populates="template")


class Page(*CustomModel):
    __tablename__ = "pages"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String, nullable=False)
    template_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("templates.id")), nullable=False
    )

    template = db.relationship("Template", back_populates="pages")
    content = db.relationship(
        "Content", back_populates="page", cascade="all, delete-orphan"
    )

    def __init__(self, name, template=None, template_id=None, *args, **kwargs):
        if template:
            self.template_id = template.id
        elif template_id:
            self.template_id = template_id
        else:
            t = Template.query.filter_by(name=name).first()
            if not t:
                t = Template(name=name)
                db.session.add(t)
                db.session.commit()
            self.template_id = t.id

        super().__init__(name=name, *args, **kwargs)


def gen_content_index(page_id):
    page = Page.query.get(int(page_id))
    if page is None:
        raise ValueError(f"Page with id {page_id} does not exist.")

    contentIds = [int(content.id.split("_")[1]) for content in page.content]

    return f"{page_id}_{max(contentIds)+1 if contentIds else 1}"


class Content(Model, *CustomModelWithoutId):
    __tablename__ = "contents"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    header = db.Column(db.String, nullable=True)
    sub_header = db.Column(db.String, nullable=True)
    text = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    link_to = db.Column(db.String, nullable=True)
    page_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("pages.id")), nullable=False
    )

    page = db.relationship("Page", back_populates="content")

    def __init__(self, page_id=None, page=None, *args, **kwargs):
        if page:
            self.id = gen_content_index(page_id=page.id)
            self.page_id = page.id
        else:
            self.id = gen_content_index(page_id=page_id)
            self.page_id = page_id
        super().__init__(*args, **kwargs)


class Affirmation(*CustomModel):
    __tablename__ = "affirmations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    affirmation = db.Column(db.String, nullable=False)


class Client(*CustomModel):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    preferred_method_of_communication = db.Column(
        db.Enum("call", "text", "email", name="preferred_type"), default="email"
    )

    location_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("locations.id")), nullable=False
    )

    location = db.relationship("Location")
    workshops = db.relationship(
        "Workshop", back_populates="client", cascade="all, delete-orphan"
    )


class ClientUser(*CustomUserModel):
    __tablename__ = "client_users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)

    client_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("clients.id")), nullable=False
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("locations.id")), nullable=False
    )

    preferred_location = db.relationship("Location")
    client = db.relationship("Client")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __init__(self, username=None, client_id=None, client=None, *args, **kwargs):
        def set_with_client(self, client):
            self.first_name = client.first_name
            self.last_name = client.last_name
            self.email = client.email
            self.location_id = client.location_id
            if not username:
                self.username = f"{client.first_name}{client.last_name}"
            else:
                self.username = username

        if client:
            set_with_client(self=self, client=client)
        elif client_id:
            set_with_client(self=self, client=Client.query.get(int(client_id)))

        super().__init__(*args, **kwargs)
