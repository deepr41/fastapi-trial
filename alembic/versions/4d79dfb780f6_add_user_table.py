"""add user table

Revision ID: 4d79dfb780f6
Revises: 735be4abc67d
Create Date: 2021-11-24 12:35:12.608663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d79dfb780f6'
down_revision = '735be4abc67d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('email', sa.String(), nullable=False),
                        sa.Column('password', sa.String(), nullable=False),
                        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                        sa.PrimaryKeyConstraint('id'),
                        sa.UniqueConstraint('email')
                        )


def downgrade():
    op.drop_table('users')
