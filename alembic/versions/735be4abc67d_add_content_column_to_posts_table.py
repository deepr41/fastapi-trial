"""add content column to posts table

Revision ID: 735be4abc67d
Revises: b45c36965b37
Create Date: 2021-11-24 12:30:07.746329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '735be4abc67d'
down_revision = 'b45c36965b37'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts','content')
