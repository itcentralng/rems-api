"""empty message

Revision ID: 08ac15f077b1
Revises: cc24c6026f2f
Create Date: 2022-11-05 16:20:51.270423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08ac15f077b1'
down_revision = 'cc24c6026f2f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('property', sa.Column('type', sa.String(), nullable=True))
    op.add_column('property', sa.Column('file_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('property', 'file_number')
    op.drop_column('property', 'type')
    # ### end Alembic commands ###
