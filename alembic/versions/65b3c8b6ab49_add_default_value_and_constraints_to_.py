"""Add default value and constraints to Funding model

Revision ID: 65b3c8b6ab49
Revises: 8122fc105985
Create Date: 2024-09-11 20:40:03.764655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65b3c8b6ab49'
down_revision = '8122fc105985'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.alter_column('invested_amount',
               existing_type=sa.INTEGER(),
               nullable=False)

    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.alter_column('invested_amount',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.alter_column('invested_amount',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.alter_column('invested_amount',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###