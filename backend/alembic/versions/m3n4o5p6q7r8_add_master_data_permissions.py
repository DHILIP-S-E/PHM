"""Add master data permissions

Revision ID: m3n4o5p6q7r8
Revises: l2m3n4o5p6q7
Create Date: 2026-01-14 07:05:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from datetime import datetime
import uuid

# revision identifiers, used by Alembic.
revision = 'm3n4o5p6q7r8'
down_revision = 'l2m3n4o5p6q7'
branch_labels = None
depends_on = None


def generate_uuid():
    return str(uuid.uuid4())


def upgrade():
    # Add missing master data permissions
    conn = op.get_bind()
    
    new_permissions = [
        # Brands
        ('brands.view', 'brands', 'view', 'global', 'View brands'),
        ('brands.create', 'brands', 'create', 'global', 'Create brands'),
        ('brands.manage', 'brands', 'manage', 'global', 'Manage brands'),
        
        # Manufacturers
        ('manufacturers.view', 'manufacturers', 'view', 'global', 'View manufacturers'),
        ('manufacturers.create', 'manufacturers', 'create', 'global', 'Create manufacturers'),
        ('manufacturers.manage', 'manufacturers', 'manage', 'global', 'Manage manufacturers'),
        
        # Medicine Types
        ('medicine_types.view', 'medicine_types', 'view', 'global', 'View medicine types'),
        ('medicine_types.create', 'medicine_types', 'create', 'global', 'Create medicine types'),
        ('medicine_types.manage', 'medicine_types', 'manage', 'global', 'Manage medicine types'),
        
        # Suppliers
        ('suppliers.view', 'suppliers', 'view', 'global', 'View suppliers'),
        ('suppliers.create', 'suppliers', 'create', 'global', 'Create suppliers'),
        ('suppliers.manage', 'suppliers', 'manage', 'global', 'Manage suppliers'),
        
        # Adjustment Reasons
        ('adjustment_reasons.view', 'adjustment_reasons', 'view', 'global', 'View adjustment reasons'),
        ('adjustment_reasons.create', 'adjustment_reasons', 'create', 'global', 'Create adjustment reasons'),
        ('adjustment_reasons.manage', 'adjustment_reasons', 'manage', 'global', 'Manage adjustment reasons'),
        
        # Payment Methods
        ('payment_methods.view', 'payment_methods', 'view', 'global', 'View payment methods'),
        ('payment_methods.create', 'payment_methods', 'create', 'global', 'Create payment methods'),
        ('payment_methods.manage', 'payment_methods', 'manage', 'global', 'Manage payment methods'),
        
        # Racks (additional manage permission)
        ('racks.manage', 'racks', 'manage', 'global', 'Manage racks globally'),
    ]
    
    # Insert new permissions
    for code, module, action, scope, description in new_permissions:
        # Check if permission already exists
        existing = conn.execute(
            text("SELECT id FROM permissions WHERE code = :code"),
            {'code': code}
        ).fetchone()
        
        if not existing:
            perm_id = generate_uuid()
            conn.execute(
                text(
                    "INSERT INTO permissions (id, code, module, action, scope, description, created_at) "
                    "VALUES (:id, :code, :module, :action, :scope, :description, :created_at)"
                ),
                {
                    'id': perm_id,
                    'code': code,
                    'module': module,
                    'action': action,
                    'scope': scope,
                    'description': description,
                    'created_at': datetime.utcnow()
                }
            )
    
    # Grant all new permissions to super_admin role
    super_admin = conn.execute(
        text("SELECT id FROM roles WHERE name = 'super_admin'")
    ).fetchone()
    
    if super_admin:
        for code, _, _, _, _ in new_permissions:
            perm = conn.execute(
                text("SELECT id FROM permissions WHERE code = :code"),
                {'code': code}
            ).fetchone()
            
            if perm:
                # Check if role already has this permission
                existing_rp = conn.execute(
                    text("SELECT id FROM role_permissions WHERE role_id = :role_id AND permission_id = :perm_id"),
                    {'role_id': super_admin[0], 'perm_id': perm[0]}
                ).fetchone()
                
                if not existing_rp:
                    conn.execute(
                        text(
                            "INSERT INTO role_permissions (id, role_id, permission_id, created_at) "
                            "VALUES (:id, :role_id, :permission_id, :created_at)"
                        ),
                        {
                            'id': generate_uuid(),
                            'role_id': super_admin[0],
                            'permission_id': perm[0],
                            'created_at': datetime.utcnow()
                        }
                    )


def downgrade():
    conn = op.get_bind()
    
    # Remove permissions
    permission_codes = [
        'brands.view', 'brands.create', 'brands.manage',
        'manufacturers.view', 'manufacturers.create', 'manufacturers.manage',
        'medicine_types.view', 'medicine_types.create', 'medicine_types.manage',
        'suppliers.view', 'suppliers.create', 'suppliers.manage',
        'adjustment_reasons.view', 'adjustment_reasons.create', 'adjustment_reasons.manage',
        'payment_methods.view', 'payment_methods.create', 'payment_methods.manage',
        'racks.manage'
    ]
    
    for code in permission_codes:
        conn.execute(
            text("DELETE FROM permissions WHERE code = :code"),
            {'code': code}
        )
