"""add last few columns to posts table

Revision ID: e8e4742278fb
Revises: e88de9a9f066
Create Date: 2021-11-24 12:54:02.383511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8e4742278fb'
down_revision = 'e88de9a9f066'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))



def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
