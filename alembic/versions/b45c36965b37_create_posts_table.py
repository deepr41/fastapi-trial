"""Create posts table

Revision ID: b45c36965b37
Revises: 
Create Date: 2021-11-24 12:24:28.304274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b45c36965b37'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
    pass
