"""empty message

Revision ID: 56aa6ee839ac
Revises: 
Create Date: 2024-10-04 03:59:58.240156

"""
from alembic import op
import sqlalchemy as sa
import os


# revision identifiers, used by Alembic.
revision = '56aa6ee839ac'
down_revision = None
branch_labels = None
depends_on = None



environment = os.getenv("FLASK_ENV")
SCHEMA = os.environ.get("SCHEMA")






def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('affirmations',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('affirmation', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locations',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('templates',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workshop_types',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('time_frame', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('clients',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('phone_number', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('preferred_method_of_communication', sa.Enum('call', 'text', 'email', name='preferred_type'), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pages',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('template_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['template_id'], ['templates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('client_users',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('contents',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('header', sa.String(), nullable=True),
    sa.Column('sub_header', sa.String(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('link_to', sa.String(), nullable=True),
    sa.Column('page_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['page_id'], ['pages.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('workshops',
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('workshop_type_id', sa.Integer(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.ForeignKeyConstraint(['workshop_type_id'], ['workshop_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    if environment == "production":
        op.execute(f"ALTER TABLE admins SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE affirmations SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE workshop_types SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE locations SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE workshops SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE templates SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE pages SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE contents SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE clients SET SCHEMA {SCHEMA};")
        op.execute(f"ALTER TABLE client_users SET SCHEMA {SCHEMA};")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('workshops')
    op.drop_table('contents')
    op.drop_table('client_users')
    op.drop_table('pages')
    op.drop_table('clients')
    op.drop_table('workshop_types')
    op.drop_table('templates')
    op.drop_table('locations')
    op.drop_table('affirmations')
    op.drop_table('admins')
    # ### end Alembic commands ###
