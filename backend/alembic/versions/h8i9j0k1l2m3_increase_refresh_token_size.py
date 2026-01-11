"""Increase refresh_token column size in sessions table

Revision ID: h8i9j0k1l2m3
Revises: g7h8i9j0k1l2
Create Date: 2026-01-11 20:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'h8i9j0k1l2m3'
down_revision = 'g7h8i9j0k1l2'
branch_labels = None
depends_on = None


def upgrade():
    # Increase refresh_token column size to accommodate JWT with permissions
    op.alter_column(
        'sessions',
        'refresh_token',
        existing_type=sa.String(500),
        type_=sa.Text(),
        existing_nullable=True
    )


def downgrade():
    # Revert to original size (may truncate data)
    op.alter_column(
        'sessions',
        'refresh_token',
        existing_type=sa.Text(),
        type_=sa.String(500),
        existing_nullable=True
    )
