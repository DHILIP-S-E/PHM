"""make email optional in employees

Revision ID: n4o5p6q7r8s9
Revises: m3n4o5p6q7r8
Create Date: 2026-01-15 17:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'n4o5p6q7r8s9'
down_revision = 'm3n4o5p6q7r8'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('employees', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)


def downgrade():
    op.alter_column('employees', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
