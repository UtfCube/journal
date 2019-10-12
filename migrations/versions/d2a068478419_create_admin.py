"""create admin

Revision ID: d2a068478419
Revises: 69fabeccdd5c
Create Date: 2019-10-13 01:12:20.297598

"""
from alembic import op
from sqlalchemy.sql import table, column
from werkzeug.security import generate_password_hash
from sqlalchemy import String, Integer, Boolean


# revision identifiers, used by Alembic.
revision = 'd2a068478419'
down_revision = '69fabeccdd5c'
branch_labels = None
depends_on = None

users_table = table('users',
    column('id', Integer),
    column('username', String),
    column('password_hash', String),
    column('role', String))


def upgrade():
    op.bulk_insert(users_table, 
        [
            {
                'id': 1,
                'username': 'admin',
                'password_hash': generate_password_hash('admin'),
                'role': 'admin'
            }
        ]
    )


def downgrade():
    pass
