from flask.cli import AppGroup
from application.models.db import db, environment, SCHEMA
from .admins import seed_admins, undo_admins
from .workshop_types import seed_workshop_types, undo_workshop_types
from .locations import seed_locations, undo_locations
from .clients import seed_clients, undo_clients
from .workshops import seed_workshops, undo_workshops
from .templates import seed_templates, undo_templates
from .pages import seed_pages, undo_pages
from .content import seed_contents, undo_contents

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup("seed")


# Creates the `flask seed all` command
@seed_commands.command("all")
def seed():
    if environment == "production":
        # Before seeding in production, you want to run the seed undo
        # command, which will  truncate all tables prefixed with
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_contents()
        undo_pages()
        undo_templates()
        undo_workshops()
        undo_clients()
        undo_locations()
        undo_workshop_types()
        undo_admins()
    seed_admins()
    seed_workshop_types()
    seed_locations()
    seed_clients()
    seed_workshops()
    seed_templates()
    seed_pages()
    seed_contents()
    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command("undo")
def undo():
    undo_contents()
    undo_pages()
    undo_templates()
    undo_workshops()
    undo_clients()
    undo_locations()
    undo_workshop_types()
    undo_admins()
    # Add other undo functions here
