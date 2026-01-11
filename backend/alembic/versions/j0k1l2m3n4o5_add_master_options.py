"""Add master_options table for configurable status/type/priority lists

Revision ID: j0k1l2m3n4o5
Revises: i9j0k1l2m3n4
Create Date: 2026-01-11 20:50:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime
import uuid

# revision identifiers, used by Alembic.
revision = 'j0k1l2m3n4o5'
down_revision = 'i9j0k1l2m3n4'
branch_labels = None
depends_on = None


def generate_uuid():
    return str(uuid.uuid4())


def upgrade():
    # Create master_options table
    op.create_table(
        'master_options',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('category', sa.String(50), nullable=False, index=True),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('label', sa.String(100), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('display_order', sa.Integer, default=0),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('is_system', sa.Boolean, default=False),
        sa.Column('color', sa.String(20)),
        sa.Column('icon', sa.String(50)),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow)
    )
    op.create_index('idx_master_option_category', 'master_options', ['category'])
    op.create_index('idx_master_option_unique', 'master_options', ['category', 'code'], unique=True)

    # Seed default options
    conn = op.get_bind()
    
    options = [
        # Entity Status (for warehouses, shops)
        ('entity_status', 'active', 'Active', 'Entity is operational', 1, True, 'green', 'check_circle'),
        ('entity_status', 'inactive', 'Inactive', 'Entity is not operational', 2, True, 'slate', 'cancel'),
        ('entity_status', 'maintenance', 'Maintenance', 'Entity under maintenance', 3, True, 'amber', 'build'),
        ('entity_status', 'suspended', 'Suspended', 'Entity is suspended', 4, True, 'red', 'block'),
        
        # Shop Types
        ('shop_type', 'retail', 'Retail Pharmacy', 'Standard retail pharmacy', 1, True, 'blue', 'storefront'),
        ('shop_type', 'wholesale', 'Wholesale', 'Wholesale distribution', 2, True, 'purple', 'warehouse'),
        ('shop_type', 'franchise', 'Franchise', 'Franchise outlet', 3, True, 'green', 'store'),
        ('shop_type', 'hospital', 'Hospital Pharmacy', 'Hospital-attached pharmacy', 4, True, 'red', 'local_hospital'),
        ('shop_type', 'clinic', 'Clinic Pharmacy', 'Clinic-attached pharmacy', 5, True, 'cyan', 'medical_services'),
        
        # Priority Levels
        ('priority', 'low', 'Low', 'Low priority', 1, True, 'slate', 'arrow_downward'),
        ('priority', 'normal', 'Normal', 'Normal priority', 2, True, 'blue', 'horizontal_rule'),
        ('priority', 'high', 'High', 'High priority', 3, True, 'amber', 'arrow_upward'),
        ('priority', 'urgent', 'Urgent', 'Urgent priority', 4, True, 'red', 'priority_high'),
        
        # Purchase Request Status
        ('request_status', 'pending', 'Pending', 'Awaiting approval', 1, True, 'amber', 'pending'),
        ('request_status', 'approved', 'Approved', 'Request approved', 2, True, 'green', 'check_circle'),
        ('request_status', 'partial', 'Partially Fulfilled', 'Partially fulfilled', 3, True, 'blue', 'incomplete_circle'),
        ('request_status', 'rejected', 'Rejected', 'Request rejected', 4, True, 'red', 'cancel'),
        ('request_status', 'completed', 'Completed', 'Fully completed', 5, True, 'green', 'task_alt'),
        ('request_status', 'dispatched', 'Dispatched', 'Items dispatched', 6, True, 'purple', 'local_shipping'),
        
        # Dispatch Status  
        ('dispatch_status', 'created', 'Created', 'Dispatch created', 1, True, 'slate', 'add_box'),
        ('dispatch_status', 'packed', 'Packed', 'Items packed', 2, True, 'blue', 'inventory_2'),
        ('dispatch_status', 'dispatched', 'Dispatched', 'In transit', 3, True, 'amber', 'local_shipping'),
        ('dispatch_status', 'in_transit', 'In Transit', 'On the way', 4, True, 'purple', 'directions_car'),
        ('dispatch_status', 'delivered', 'Delivered', 'Successfully delivered', 5, True, 'green', 'check_circle'),
        ('dispatch_status', 'cancelled', 'Cancelled', 'Dispatch cancelled', 6, True, 'red', 'cancel'),
        
        # Invoice Status
        ('invoice_status', 'draft', 'Draft', 'Draft invoice', 1, True, 'slate', 'edit'),
        ('invoice_status', 'completed', 'Completed', 'Invoice completed', 2, True, 'green', 'check_circle'),
        ('invoice_status', 'cancelled', 'Cancelled', 'Invoice cancelled', 3, True, 'red', 'cancel'),
        ('invoice_status', 'returned', 'Returned', 'Items returned', 4, True, 'amber', 'assignment_return'),
        
        # Payment Status
        ('payment_status', 'pending', 'Pending', 'Payment pending', 1, True, 'amber', 'pending'),
        ('payment_status', 'partial', 'Partial', 'Partially paid', 2, True, 'blue', 'incomplete_circle'),
        ('payment_status', 'completed', 'Completed', 'Fully paid', 3, True, 'green', 'payments'),
        ('payment_status', 'refunded', 'Refunded', 'Payment refunded', 4, True, 'purple', 'currency_exchange'),
        
        # Attendance Status
        ('attendance_status', 'present', 'Present', 'Employee present', 1, True, 'green', 'check_circle'),
        ('attendance_status', 'absent', 'Absent', 'Employee absent', 2, True, 'red', 'cancel'),
        ('attendance_status', 'half_day', 'Half Day', 'Half day attendance', 3, True, 'amber', 'timelapse'),
        ('attendance_status', 'leave', 'On Leave', 'Employee on leave', 4, True, 'blue', 'event_busy'),
        
        # Medicine Types
        ('medicine_type', 'tablet', 'Tablet', 'Oral tablet', 1, True, 'blue', 'medication'),
        ('medicine_type', 'capsule', 'Capsule', 'Oral capsule', 2, True, 'green', 'medication'),
        ('medicine_type', 'syrup', 'Syrup', 'Liquid syrup', 3, True, 'amber', 'local_drink'),
        ('medicine_type', 'injection', 'Injection', 'Injectable', 4, True, 'red', 'vaccines'),
        ('medicine_type', 'cream', 'Cream', 'Topical cream', 5, True, 'purple', 'spa'),
        ('medicine_type', 'ointment', 'Ointment', 'Topical ointment', 6, True, 'cyan', 'spa'),
        ('medicine_type', 'drops', 'Drops', 'Eye/Ear drops', 7, True, 'teal', 'water_drop'),
        ('medicine_type', 'powder', 'Powder', 'Powder form', 8, True, 'slate', 'grain'),
        ('medicine_type', 'other', 'Other', 'Other type', 9, True, 'slate', 'more_horiz'),
        
        # Notification Types
        ('notification_type', 'info', 'Information', 'General information', 1, True, 'blue', 'info'),
        ('notification_type', 'success', 'Success', 'Success notification', 2, True, 'green', 'check_circle'),
        ('notification_type', 'warning', 'Warning', 'Warning notification', 3, True, 'amber', 'warning'),
        ('notification_type', 'error', 'Error', 'Error notification', 4, True, 'red', 'error'),
        ('notification_type', 'stock', 'Low Stock', 'Stock alert', 5, True, 'amber', 'inventory'),
        ('notification_type', 'expiry', 'Expiry', 'Expiry alert', 6, True, 'red', 'event'),
    ]
    
    for category, code, label, description, order, is_system, color, icon in options:
        conn.execute(
            sa.text(
                """INSERT INTO master_options 
                (id, category, code, label, description, display_order, is_active, is_system, color, icon, created_at) 
                VALUES (:id, :category, :code, :label, :description, :display_order, :is_active, :is_system, :color, :icon, :created_at)"""
            ),
            {
                'id': generate_uuid(),
                'category': category,
                'code': code,
                'label': label,
                'description': description,
                'display_order': order,
                'is_active': True,
                'is_system': is_system,
                'color': color,
                'icon': icon,
                'created_at': datetime.utcnow()
            }
        )


def downgrade():
    op.drop_index('idx_master_option_unique', 'master_options')
    op.drop_index('idx_master_option_category', 'master_options')
    op.drop_table('master_options')
