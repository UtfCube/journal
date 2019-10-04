"""empty message

Revision ID: d293b0801bcc
Revises: dd418c6080ae
Create Date: 2019-10-02 17:00:20.603432

"""
from alembic import op
from sqlalchemy.sql import table, column
from werkzeug.security import generate_password_hash
from sqlalchemy import String, Integer, Boolean


# revision identifiers, used by Alembic.
revision = 'd293b0801bcc'
down_revision = 'dd418c6080ae'
branch_labels = None
depends_on = None


users_table = table('users',
    column('id', Integer),
    column('username', String),
    column('password_hash', String),
    column('is_admin', Boolean))


def upgrade():
    op.bulk_insert(users_table, 
        [
            {
                'id': 1,
                'username': 'admin',
                'password_hash': generate_password_hash('admin'),
                'is_admin': True
            }
        ]
    )


def downgrade():
    pass