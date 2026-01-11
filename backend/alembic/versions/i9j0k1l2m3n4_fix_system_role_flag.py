"""Fix is_system flag - only super_admin should be system role

Revision ID: i9j0k1l2m3n4
Revises: h8i9j0k1l2m3
Create Date: 2026-01-11 20:37:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'i9j0k1l2m3n4'
down_revision = 'h8i9j0k1l2m3'
branch_labels = None
depends_on = None


def upgrade():
    # Only super_admin should be a system role
    # Other roles should be editable (is_system=False)
    conn = op.get_bind()
    
    # Set is_system=False for all roles except super_admin
    conn.execute(
        sa.text(
            "UPDATE roles SET is_system = FALSE WHERE name != 'super_admin'"
        )
    )


def downgrade():
    # Revert all seeded roles to is_system=True
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "UPDATE roles SET is_system = TRUE WHERE name IN ('super_admin', 'warehouse_admin', 'warehouse_employee', 'pharmacy_admin', 'pharmacy_employee')"
        )
    )
