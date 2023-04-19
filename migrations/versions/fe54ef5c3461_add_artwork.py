"""add artwork

Revision ID: fe54ef5c3461
Revises: 1aca3636d6c6
Create Date: 2023-04-18 15:32:36.918724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe54ef5c3461'
down_revision = '1aca3636d6c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artwork',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image', sa.LargeBinary(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('artwork_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artwork_id'], ['art.art_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artwork')
    # ### end Alembic commands ###