from .jsonable import JSONable
from flask_login import UserMixin
from .timestamps import Timestamps
from .db import db, add_prefix_for_prod
from .id import ID
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

Model = db.Model


CustomModel = (Model, Timestamps, ID, JSONable)
CustomUserModel = (Model, UserMixin, Timestamps, ID, JSONable)
CustomModelWithoutId = (Timestamps, JSONable)


"""
The website will only support logins for those that can edit the website
"""


class Admin(*CustomUserModel):
    __tablename__ = "admins"
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
    type = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    time_frame = db.Column(db.Float, nullable=False)

    # workshop_instances = db.relationship("Workshop", back_populates="workshop_type")


class Location(*CustomModel):
    __tablename__ = "locations"
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)


class Workshop(*CustomModel):
    __tablename__ = "workshops"
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

    workshop_type = db.relationship(
        "WorkshopType",
        backref="workshop_instances",
        primaryjoin=f"{add_prefix_for_prod("workshops.workshop_type_id")} == {add_prefix_for_prod("workshop_types.id")}",
    )
    location = db.relationship("Location")
    client = db.relationship("Client", backref="workshops")

    @property
    def start(self):
        return self.get_timestamp_breakdown("start_date")

    @property
    def end(self):
        return self.get_timestamp_breakdown("end_date")

    def __init__(
        self,
        workshop_type=None,
        start_date=None,
        workshop_type_id=None,
        client=None,
        client_id=None,
        *args,
        **kwargs,
    ):
        duration = 0.0
        if workshop_type:
            self.workshop_type_id = workshop_type.id
            duration = workshop_type.time_frame
        elif workshop_type_id:
            workshop_type = WorkshopType.query.get(int(workshop_type_id))
            self.workshop_type_id = workshop_type_id
            duration = workshop_type.time_frame

        seconds = duration * 60 * 60

        if isinstance(start_date, datetime):
            end_date = start_date + timedelta(seconds=seconds)
            self.start_date = start_date
        elif isinstance(start_date, str):
            end_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S") + timedelta(
                seconds=seconds
            )
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")

        self.end_date = end_date

        if client:
            self.client_id = client.id
            self.location_id = client.location_id
        elif client_id:
            client = Client.query.get(int(client_id))
            self.client_id = client_id
            self.location_id = client.location_id

        super().__init__(*args, **kwargs)


"""
The Following Models are all used to store the content on each page in the backend
The templates table will only be updated when a new template component is created on the frontend
The name of the Template will be the same as the name of the component on the frontend
"""


class Template(*CustomModel):
    __tablename__ = "templates"
    name = db.Column(db.String, nullable=False)


class Page(*CustomModel):
    __tablename__ = "pages"
    is_public = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String, nullable=False)
    template_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("templates.id")), nullable=False
    )

    template = db.relationship("Template", backref="pages")
    # content = db.relationship("Content", back_populates="page")

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
            template_id = t.id

        super().__init__(name=name, *args, **kwargs)


def gen_content_index(page_id):
    page = Page.query.get(int(page_id))
    if page is None:
        raise ValueError(f"Page with id {page_id} does not exist.")
    return f"{page_id}_{len(page.content)}"


class Content(Model, *CustomModelWithoutId):
    __tablename__ = "contents"
    id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    header = db.Column(db.String, nullable=True)
    sub_header = db.Column(db.String, nullable=True)
    text = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String, nullable=True)
    link_to = db.Column(db.String, nullable=True)
    page_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("pages.id")), nullable=False
    )

    page = db.relationship("Page", backref="content")

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
    affirmation = db.Column(db.String, nullable=False)


class Client(*CustomModel):
    __tablename__ = "clients"
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
    # workshops = db.relationship("Workshop", back_populates="client")


class ClientUser(*CustomUserModel):
    __tablename__ = "client_users"
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
