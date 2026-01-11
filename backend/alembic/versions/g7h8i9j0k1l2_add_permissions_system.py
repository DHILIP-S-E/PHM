"""Add permissions system with Permission, RolePermission, and updated Role/User models

Revision ID: g7h8i9j0k1l2
Revises: 6cbf7e558e1c
Create Date: 2026-01-11 20:10:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
import uuid

# revision identifiers, used by Alembic.
revision = 'g7h8i9j0k1l2'
down_revision = '6cbf7e558e1c'
branch_labels = None
depends_on = None


def generate_uuid():
    return str(uuid.uuid4())


def upgrade():
    # Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('code', sa.String(100), unique=True, nullable=False, index=True),
        sa.Column('module', sa.String(50), nullable=False),
        sa.Column('action', sa.String(50), nullable=False),
        sa.Column('scope', sa.String(20), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow)
    )
    op.create_index('idx_permission_module', 'permissions', ['module', 'action'])

    # Create role_permissions junction table
    op.create_table(
        'role_permissions',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('role_id', sa.String(36), sa.ForeignKey('roles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('permission_id', sa.String(36), sa.ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow)
    )
    op.create_index('idx_role_permission', 'role_permissions', ['role_id', 'permission_id'], unique=True)

    # Add new columns to roles table
    op.add_column('roles', sa.Column('entity_type', sa.String(20), nullable=True))
    op.add_column('roles', sa.Column('is_creatable', sa.Boolean, default=True, server_default='1'))

    # Add role_id FK to users table
    op.add_column('users', sa.Column('role_id', sa.String(36), sa.ForeignKey('roles.id'), nullable=True))

    # Seed default permissions
    permissions = [
        # Dashboard
        ('dashboard.view', 'dashboard', 'view', 'global', 'View dashboard'),
        
        # User Management
        ('users.view', 'users', 'view', 'global', 'View users list'),
        ('users.create', 'users', 'create', 'global', 'Create new users'),
        ('users.edit', 'users', 'edit', 'global', 'Edit users'),
        ('users.delete', 'users', 'delete', 'global', 'Delete users'),
        
        # Roles Management
        ('roles.view', 'roles', 'view', 'global', 'View roles'),
        ('roles.manage', 'roles', 'manage', 'global', 'Manage roles and permissions'),
        
        # Warehouse Management
        ('warehouses.view', 'warehouses', 'view', 'global', 'View all warehouses'),
        ('warehouses.create', 'warehouses', 'create', 'global', 'Create warehouses'),
        ('warehouses.edit', 'warehouses', 'edit', 'global', 'Edit warehouses'),
        ('warehouses.delete', 'warehouses', 'delete', 'global', 'Delete warehouses'),
        
        # Shop Management  
        ('shops.view', 'shops', 'view', 'global', 'View all shops'),
        ('shops.create', 'shops', 'create', 'global', 'Create shops'),
        ('shops.edit', 'shops', 'edit', 'global', 'Edit shops'),
        ('shops.delete', 'shops', 'delete', 'global', 'Delete shops'),
        
        # Medicine Master
        ('medicines.view', 'medicines', 'view', 'global', 'View medicines catalog'),
        ('medicines.create', 'medicines', 'create', 'global', 'Create medicines'),
        ('medicines.edit', 'medicines', 'edit', 'global', 'Edit medicines'),
        ('medicines.delete', 'medicines', 'delete', 'global', 'Delete medicines'),
        
        # Categories/Units/HSN/GST
        ('categories.manage', 'categories', 'manage', 'global', 'Manage medicine categories'),
        ('units.manage', 'units', 'manage', 'global', 'Manage units'),
        ('hsn.manage', 'hsn', 'manage', 'global', 'Manage HSN codes'),
        ('gst.manage', 'gst', 'manage', 'global', 'Manage GST/VAT settings'),
        
        # Inventory - Global Scope (Super Admin)
        ('inventory.view.global', 'inventory', 'view', 'global', 'View all inventory across system'),
        ('inventory.oversight', 'inventory', 'oversight', 'global', 'Inventory oversight dashboard'),
        
        # Inventory - Warehouse Scope
        ('inventory.view.warehouse', 'inventory', 'view', 'warehouse', 'View warehouse inventory'),
        ('inventory.adjust.warehouse', 'inventory', 'adjust', 'warehouse', 'Adjust warehouse inventory'),
        ('inventory.entry.warehouse', 'inventory', 'entry', 'warehouse', 'Stock entry to warehouse'),
        
        # Inventory - Shop Scope
        ('inventory.view.shop', 'inventory', 'view', 'shop', 'View shop inventory'),
        ('inventory.adjust.shop', 'inventory', 'adjust', 'shop', 'Adjust shop inventory'),
        
        # Racks
        ('racks.view', 'racks', 'view', 'global', 'View racks'),
        ('racks.manage.warehouse', 'racks', 'manage', 'warehouse', 'Manage warehouse racks'),
        
        # Purchase Requests
        ('purchase_requests.view.global', 'purchase_requests', 'view', 'global', 'View all purchase requests'),
        ('purchase_requests.view.warehouse', 'purchase_requests', 'view', 'warehouse', 'View warehouse purchase requests'),
        ('purchase_requests.view.shop', 'purchase_requests', 'view', 'shop', 'View shop purchase requests'),
        ('purchase_requests.create.shop', 'purchase_requests', 'create', 'shop', 'Create purchase requests from shop'),
        ('purchase_requests.approve.warehouse', 'purchase_requests', 'approve', 'warehouse', 'Approve purchase requests'),
        
        # Dispatches
        ('dispatches.view.global', 'dispatches', 'view', 'global', 'View all dispatches'),
        ('dispatches.view.warehouse', 'dispatches', 'view', 'warehouse', 'View warehouse dispatches'),
        ('dispatches.view.shop', 'dispatches', 'view', 'shop', 'View shop dispatches'),
        ('dispatches.create.warehouse', 'dispatches', 'create', 'warehouse', 'Create dispatches from warehouse'),
        
        # Billing/POS
        ('billing.view.shop', 'billing', 'view', 'shop', 'View billing/invoices'),
        ('billing.create.shop', 'billing', 'create', 'shop', 'Create bills/POS'),
        ('billing.void.shop', 'billing', 'void', 'shop', 'Void invoices'),
        
        # Returns
        ('returns.view.shop', 'returns', 'view', 'shop', 'View returns'),
        ('returns.create.shop', 'returns', 'create', 'shop', 'Process returns'),
        
        # Customers
        ('customers.view', 'customers', 'view', 'global', 'View customers'),
        ('customers.view.shop', 'customers', 'view', 'shop', 'View shop customers'),
        ('customers.manage.shop', 'customers', 'manage', 'shop', 'Manage shop customers'),
        
        # Employees/HR
        ('employees.view.global', 'employees', 'view', 'global', 'View all employees'),
        ('employees.view.warehouse', 'employees', 'view', 'warehouse', 'View warehouse employees'),
        ('employees.view.shop', 'employees', 'view', 'shop', 'View shop employees'),
        ('employees.manage.warehouse', 'employees', 'manage', 'warehouse', 'Manage warehouse employees'),
        ('employees.manage.shop', 'employees', 'manage', 'shop', 'Manage shop employees'),
        ('attendance.manage.warehouse', 'attendance', 'manage', 'warehouse', 'Manage warehouse attendance'),
        ('attendance.manage.shop', 'attendance', 'manage', 'shop', 'Manage shop attendance'),
        ('salary.manage.warehouse', 'salary', 'manage', 'warehouse', 'Manage warehouse salaries'),
        ('salary.manage.shop', 'salary', 'manage', 'shop', 'Manage shop salaries'),
        
        # Reports
        ('reports.view.global', 'reports', 'view', 'global', 'View all reports'),
        ('reports.view.warehouse', 'reports', 'view', 'warehouse', 'View warehouse reports'),
        ('reports.view.shop', 'reports', 'view', 'shop', 'View shop reports'),
        ('reports.export', 'reports', 'export', 'global', 'Export reports'),
        
        # Settings
        ('settings.view', 'settings', 'view', 'global', 'View settings'),
        ('settings.manage', 'settings', 'manage', 'global', 'Manage settings'),
        
        # Audit
        ('audit.view', 'audit', 'view', 'global', 'View audit logs'),
        ('login_activity.view', 'login_activity', 'view', 'global', 'View login activity'),
        
        # Notifications
        ('notifications.view', 'notifications', 'view', 'global', 'View notifications'),
    ]
    
    # Insert permissions
    conn = op.get_bind()
    for code, module, action, scope, description in permissions:
        perm_id = generate_uuid()
        conn.execute(
            sa.text(
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

    # Seed system roles
    roles = [
        ('super_admin', 'Super Administrator', None, True, False, 'Full system access'),
        ('warehouse_admin', 'Warehouse Administrator', 'warehouse', True, True, 'Warehouse management access'),
        ('warehouse_employee', 'Warehouse Employee', 'warehouse', True, True, 'Basic warehouse operations'),
        ('pharmacy_admin', 'Pharmacy Administrator', 'shop', True, True, 'Pharmacy/shop management access'),
        ('pharmacy_employee', 'Pharmacy Employee', 'shop', True, True, 'Basic pharmacy operations'),
    ]
    
    role_ids = {}
    for name, display_name, entity_type, is_system, is_creatable, description in roles:
        role_id = generate_uuid()
        role_ids[name] = role_id
        conn.execute(
            sa.text(
                "INSERT INTO roles (id, name, description, entity_type, is_system, is_creatable, created_at) "
                "VALUES (:id, :name, :description, :entity_type, :is_system, :is_creatable, :created_at)"
            ),
            {
                'id': role_id,
                'name': name,
                'description': description,
                'entity_type': entity_type,
                'is_system': is_system,
                'is_creatable': is_creatable,
                'created_at': datetime.utcnow()
            }
        )
    
    # Assign ALL permissions to super_admin
    all_perms = conn.execute(sa.text("SELECT id FROM permissions")).fetchall()
    for perm in all_perms:
        conn.execute(
            sa.text(
                "INSERT INTO role_permissions (id, role_id, permission_id, created_at) "
                "VALUES (:id, :role_id, :permission_id, :created_at)"
            ),
            {
                'id': generate_uuid(),
                'role_id': role_ids['super_admin'],
                'permission_id': perm[0],
                'created_at': datetime.utcnow()
            }
        )
    
    # Assign warehouse permissions to warehouse_admin
    warehouse_admin_perms = [
        'dashboard.view', 'inventory.view.warehouse', 'inventory.adjust.warehouse', 'inventory.entry.warehouse',
        'racks.view', 'racks.manage.warehouse', 'medicines.view', 'purchase_requests.view.warehouse',
        'purchase_requests.approve.warehouse', 'dispatches.view.warehouse', 'dispatches.create.warehouse',
        'employees.view.warehouse', 'employees.manage.warehouse', 'attendance.manage.warehouse',
        'salary.manage.warehouse', 'reports.view.warehouse', 'notifications.view'
    ]
    for code in warehouse_admin_perms:
        perm = conn.execute(
            sa.text("SELECT id FROM permissions WHERE code = :code"), {'code': code}
        ).fetchone()
        if perm:
            conn.execute(
                sa.text(
                    "INSERT INTO role_permissions (id, role_id, permission_id, created_at) "
                    "VALUES (:id, :role_id, :permission_id, :created_at)"
                ),
                {
                    'id': generate_uuid(),
                    'role_id': role_ids['warehouse_admin'],
                    'permission_id': perm[0],
                    'created_at': datetime.utcnow()
                }
            )
    
    # Assign warehouse employee permissions (subset)
    warehouse_employee_perms = [
        'dashboard.view', 'inventory.view.warehouse', 'inventory.entry.warehouse',
        'racks.view', 'medicines.view', 'dispatches.view.warehouse', 'notifications.view'
    ]
    for code in warehouse_employee_perms:
        perm = conn.execute(
            sa.text("SELECT id FROM permissions WHERE code = :code"), {'code': code}
        ).fetchone()
        if perm:
            conn.execute(
                sa.text(
                    "INSERT INTO role_permissions (id, role_id, permission_id, created_at) "
                    "VALUES (:id, :role_id, :permission_id, :created_at)"
                ),
                {
                    'id': generate_uuid(),
                    'role_id': role_ids['warehouse_employee'],
                    'permission_id': perm[0],
                    'created_at': datetime.utcnow()
                }
            )
    
    # Assign pharmacy admin permissions
    pharmacy_admin_perms = [
        'dashboard.view', 'inventory.view.shop', 'inventory.adjust.shop', 'medicines.view',
        'purchase_requests.view.shop', 'purchase_requests.create.shop', 'dispatches.view.shop',
        'billing.view.shop', 'billing.create.shop', 'billing.void.shop', 'returns.view.shop',
        'returns.create.shop', 'customers.view.shop', 'customers.manage.shop',
        'employees.view.shop', 'employees.manage.shop', 'attendance.manage.shop',
        'salary.manage.shop', 'reports.view.shop', 'notifications.view'
    ]
    for code in pharmacy_admin_perms:
        perm = conn.execute(
            sa.text("SELECT id FROM permissions WHERE code = :code"), {'code': code}
        ).fetchone()
        if perm:
            conn.execute(
                sa.text(
                    "INSERT INTO role_permissions (id, role_id, permission_id, created_at) "
                    "VALUES (:id, :role_id, :permission_id, :created_at)"
                ),
                {
                    'id': generate_uuid(),
                    'role_id': role_ids['pharmacy_admin'],
                    'permission_id': perm[0],
                    'created_at': datetime.utcnow()
                }
            )
    
    # Assign pharmacy employee permissions (subset)
    pharmacy_employee_perms = [
        'dashboard.view', 'inventory.view.shop', 'medicines.view', 'dispatches.view.shop',
        'billing.view.shop', 'billing.create.shop', 'returns.view.shop', 'customers.view.shop',
        'notifications.view'
    ]
    for code in pharmacy_employee_perms:
        perm = conn.execute(
            sa.text("SELECT id FROM permissions WHERE code = :code"), {'code': code}
        ).fetchone()
        if perm:
            conn.execute(
                sa.text(
                    "INSERT INTO role_permissions (id, role_id, permission_id, created_at) "
                    "VALUES (:id, :role_id, :permission_id, :created_at)"
                ),
                {
                    'id': generate_uuid(),
                    'role_id': role_ids['pharmacy_employee'],
                    'permission_id': perm[0],
                    'created_at': datetime.utcnow()
                }
            )


def downgrade():
    # Remove role_id from users
    op.drop_column('users', 'role_id')
    
    # Remove new columns from roles
    op.drop_column('roles', 'is_creatable')
    op.drop_column('roles', 'entity_type')
    
    # Drop role_permissions table
    op.drop_index('idx_role_permission', 'role_permissions')
    op.drop_table('role_permissions')
    
    # Drop permissions table
    op.drop_index('idx_permission_module', 'permissions')
    op.drop_table('permissions')
