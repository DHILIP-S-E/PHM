"""Add shop statuses to status_master

Revision ID: l2m3n4o5p6q7
Revises: k1l2m3n4o5p6
Create Date: 2026-01-13 18:50:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
import uuid

# revision identifiers, used by Alembic.
revision = 'l2m3n4o5p6q7'
down_revision = 'k1l2m3n4o5p6'
branch_labels = None
depends_on = None


def generate_uuid():
    return str(uuid.uuid4())


def upgrade():
    conn = op.get_bind()

    # Check if shop statuses already exist
    result = conn.execute(text("SELECT COUNT(*) FROM status_master WHERE entity_type = 'shop'"))
    count = result.scalar()
    
    if count == 0:
        # Seed Status Master - Shop statuses
        conn.execute(text("""
            INSERT INTO status_master (id, entity_type, code, name, color, is_terminal, is_default, is_active, sort_order) VALUES
            (:id1, 'shop', 'active', 'Active', 'green', false, true, true, 1),
            (:id2, 'shop', 'inactive', 'Inactive', 'gray', false, false, true, 2),
            (:id3, 'shop', 'suspended', 'Suspended', 'orange', false, false, true, 3),
            (:id4, 'shop', 'closed', 'Permanently Closed', 'red', true, false, true, 4)
        """), {
            'id1': generate_uuid(), 'id2': generate_uuid(),
            'id3': generate_uuid(), 'id4': generate_uuid()
        })

    # Check if warehouse statuses already exist
    result = conn.execute(text("SELECT COUNT(*) FROM status_master WHERE entity_type = 'warehouse'"))
    count = result.scalar()
    
    if count == 0:
        # Seed Status Master - Warehouse statuses
        conn.execute(text("""
            INSERT INTO status_master (id, entity_type, code, name, color, is_terminal, is_default, is_active, sort_order) VALUES
            (:id1, 'warehouse', 'active', 'Active', 'green', false, true, true, 1),
            (:id2, 'warehouse', 'inactive', 'Inactive', 'gray', false, false, true, 2),
            (:id3, 'warehouse', 'maintenance', 'Under Maintenance', 'orange', false, false, true, 3),
            (:id4, 'warehouse', 'closed', 'Permanently Closed', 'red', true, false, true, 4)
        """), {
            'id1': generate_uuid(), 'id2': generate_uuid(),
            'id3': generate_uuid(), 'id4': generate_uuid()
        })

    # Check if user statuses already exist
    result = conn.execute(text("SELECT COUNT(*) FROM status_master WHERE entity_type = 'user'"))
    count = result.scalar()
    
    if count == 0:
        # Seed Status Master - User statuses
        conn.execute(text("""
            INSERT INTO status_master (id, entity_type, code, name, color, is_terminal, is_default, is_active, sort_order) VALUES
            (:id1, 'user', 'active', 'Active', 'green', false, true, true, 1),
            (:id2, 'user', 'inactive', 'Inactive', 'gray', false, false, true, 2),
            (:id3, 'user', 'suspended', 'Suspended', 'orange', false, false, true, 3),
            (:id4, 'user', 'terminated', 'Terminated', 'red', true, false, true, 4)
        """), {
            'id1': generate_uuid(), 'id2': generate_uuid(),
            'id3': generate_uuid(), 'id4': generate_uuid()
        })

    # Check if medicine statuses already exist
    result = conn.execute(text("SELECT COUNT(*) FROM status_master WHERE entity_type = 'medicine'"))
    count = result.scalar()
    
    if count == 0:
        # Seed Status Master - Medicine statuses
        conn.execute(text("""
            INSERT INTO status_master (id, entity_type, code, name, color, is_terminal, is_default, is_active, sort_order) VALUES
            (:id1, 'medicine', 'active', 'Active', 'green', false, true, true, 1),
            (:id2, 'medicine', 'inactive', 'Inactive', 'gray', false, false, true, 2),
            (:id3, 'medicine', 'discontinued', 'Discontinued', 'red', true, false, true, 3)
        """), {
            'id1': generate_uuid(), 'id2': generate_uuid(),
            'id3': generate_uuid()
        })


def downgrade():
    conn = op.get_bind()
    conn.execute(text("DELETE FROM status_master WHERE entity_type IN ('shop', 'warehouse', 'user', 'medicine')"))
