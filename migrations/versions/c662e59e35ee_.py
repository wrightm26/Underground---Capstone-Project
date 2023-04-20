"""empty message

Revision ID: c662e59e35ee
Revises: 13620aa99955
Create Date: 2023-04-20 15:11:44.670393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c662e59e35ee'
down_revision = '13620aa99955'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('art', schema=None) as batch_op:
        batch_op.add_column(sa.Column('stripe_product_id', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('art', schema=None) as batch_op:
        batch_op.drop_column('stripe_product_id')

    # ### end Alembic commands ###