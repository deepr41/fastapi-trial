"""add foreign-key to posts table

Revision ID: e88de9a9f066
Revises: 4d79dfb780f6
Create Date: 2021-11-24 12:43:25.103903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e88de9a9f066'
down_revision = '4d79dfb780f6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key("post_users_fkey", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")


def downgrade():
    op.drop_constraint('post_users_fkey', table_name="posts")
    op.drop_column('posts','owner_id')

