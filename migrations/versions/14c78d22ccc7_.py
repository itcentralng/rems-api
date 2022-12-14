"""empty message

Revision ID: 14c78d22ccc7
Revises: 5120f7743b77
Create Date: 2022-11-03 16:14:47.391645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14c78d22ccc7'
down_revision = '5120f7743b77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tenancy_cycle',
    sa.Column('unit_id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=False),
    sa.Column('cycle', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenant.id'], ),
    sa.ForeignKeyConstraint(['unit_id'], ['unit.id'], ),
    sa.PrimaryKeyConstraint('unit_id', 'tenant_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tenancy_cycle')
    # ### end Alembic commands ###
