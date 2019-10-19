"""add cascade delete

Revision ID: 7ffa31eaaff1
Revises: d2a068478419
Create Date: 2019-10-13 02:15:09.435611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ffa31eaaff1'
down_revision = 'd2a068478419'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('checkpoints_fields_checkpoint_id_fkey', 'checkpoints_fields', type_='foreignkey')
    op.create_foreign_key(None, 'checkpoints_fields', 'checkpoints', ['checkpoint_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('progress_checkpoint_field_id_fkey', 'progress', type_='foreignkey')
    op.create_foreign_key(None, 'progress', 'checkpoints_fields', ['checkpoint_field_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'progress', type_='foreignkey')
    op.create_foreign_key('progress_checkpoint_field_id_fkey', 'progress', 'checkpoints_fields', ['checkpoint_field_id'], ['id'])
    op.drop_constraint(None, 'checkpoints_fields', type_='foreignkey')
    op.create_foreign_key('checkpoints_fields_checkpoint_id_fkey', 'checkpoints_fields', 'checkpoints', ['checkpoint_id'], ['id'])
    # ### end Alembic commands ###