"""empty message

Revision ID: a10b81755c33
Revises: 08ac15f077b1
Create Date: 2022-11-06 13:47:59.330411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a10b81755c33'
down_revision = '08ac15f077b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('type', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction', 'type')
    # ### end Alembic commands ###
