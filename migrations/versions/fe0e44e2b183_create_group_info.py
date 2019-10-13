"""create group info

Revision ID: fe0e44e2b183
Revises: 7ffa31eaaff1
Create Date: 2019-10-13 14:56:07.265948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe0e44e2b183'
down_revision = '7ffa31eaaff1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('groups_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tgs_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tgs_id'], ['tgs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('dates_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_info_id', sa.Integer(), nullable=False),
    sa.Column('date_field_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=40), nullable=True),
    sa.ForeignKeyConstraint(['date_field_id'], ['checkpoints_fields.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['group_info_id'], ['groups_info.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dates_info')
    op.drop_table('groups_info')
    # ### end Alembic commands ###
