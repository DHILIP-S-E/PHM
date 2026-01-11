"""Add SSOT master tables

Revision ID: k1l2m3n4o5p6
Revises: j0k1l2m3n4o5
Create Date: 2026-01-11 21:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
import uuid

# revision identifiers, used by Alembic.
revision = 'k1l2m3n4o5p6'
down_revision = 'j0k1l2m3n4o5'
branch_labels = None
depends_on = None


def generate_uuid():
    return str(uuid.uuid4())


def upgrade():
    # Create PaymentMethodMaster table
    op.create_table(
        'payment_method_master',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('code', sa.String(20), unique=True, nullable=False, index=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('icon', sa.String(50)),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('sort_order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Create ShopTypeMaster table
    op.create_table(
        'shop_type_master',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('code', sa.String(20), unique=True, nullable=False, index=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('sort_order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Create CustomerTypeMaster table
    op.create_table(
        'customer_type_master',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('code', sa.String(20), unique=True, nullable=False, index=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('discount_percent', sa.Float(), default=0.0),
        sa.Column('credit_limit', sa.Float(), default=0.0),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('sort_order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Create MedicineTypeMaster table
    op.create_table(
        'medicine_type_master',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('code', sa.String(20), unique=True, nullable=False, index=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('sort_order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Create GSTSlabMaster table
    op.create_table(
        'gst_slab_master',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('rate', sa.Float(), unique=True, nullable=False),
        sa.Column('cgst_rate', sa.Float(), nullable=False),
        sa.Column('sgst_rate', sa.Float(), nullable=False),
        sa.Column('igst_rate', sa.Float(), nullable=False),
        sa.Column('description', sa.String(100)),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Create GenderMaster table
    op.create_table(
        'gender_master',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('code', sa.String(10), unique=True, nullable=False, index=True),
        sa.Column('name', sa.String(20), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('sort_order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Create EmploymentTypeMaster table
    op.create_table(
        'employment_type_master',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('code', sa.String(20), unique=True, nullable=False, index=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('sort_order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Create UrgencyMaster table
    op.create_table(
        'urgency_master',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('code', sa.String(20), unique=True, nullable=False, index=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('color', sa.String(20)),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('sort_order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Create StatusMaster table
    op.create_table(
        'status_master',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('entity_type', sa.String(50), nullable=False, index=True),
        sa.Column('code', sa.String(30), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('color', sa.String(20)),
        sa.Column('is_terminal', sa.Boolean(), default=False),
        sa.Column('is_default', sa.Boolean(), default=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('sort_order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index('idx_status_entity', 'status_master', ['entity_type', 'code'], unique=True)

    # Create DesignationMaster table
    op.create_table(
        'designation_master',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('code', sa.String(30), unique=True, nullable=False, index=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('level', sa.Integer(), default=1),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('sort_order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # Create DepartmentMaster table
    op.create_table(
        'department_master',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('code', sa.String(30), unique=True, nullable=False, index=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('sort_order', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    # ==================== SEED DEFAULT DATA ====================
    conn = op.get_bind()

    # Seed Payment Methods
    conn.execute(text("""
        INSERT INTO payment_method_master (id, code, name, icon, is_active, sort_order) VALUES
        (:id1, 'cash', 'Cash', '💵', true, 1),
        (:id2, 'card', 'Credit/Debit Card', '💳', true, 2),
        (:id3, 'upi', 'UPI', '📱', true, 3),
        (:id4, 'wallet', 'Wallet', '👛', true, 4),
        (:id5, 'credit', 'Store Credit', '📝', true, 5),
        (:id6, 'insurance', 'Insurance', '🏥', true, 6)
    """), {
        'id1': generate_uuid(), 'id2': generate_uuid(), 'id3': generate_uuid(),
        'id4': generate_uuid(), 'id5': generate_uuid(), 'id6': generate_uuid()
    })

    # Seed Shop Types
    conn.execute(text("""
        INSERT INTO shop_type_master (id, code, name, description, is_active, sort_order) VALUES
        (:id1, 'retail', 'Retail Pharmacy', 'Standard retail medical shop', true, 1),
        (:id2, 'wholesale', 'Wholesale Distributor', 'Bulk medicine distributor', true, 2),
        (:id3, 'hospital', 'Hospital Pharmacy', 'In-hospital pharmacy', true, 3),
        (:id4, 'clinic', 'Clinic Dispensary', 'Small clinic attached pharmacy', true, 4),
        (:id5, 'chain', 'Chain Store', 'Part of a pharmacy chain', true, 5)
    """), {
        'id1': generate_uuid(), 'id2': generate_uuid(), 'id3': generate_uuid(),
        'id4': generate_uuid(), 'id5': generate_uuid()
    })

    # Seed Customer Types
    conn.execute(text("""
        INSERT INTO customer_type_master (id, code, name, discount_percent, credit_limit, is_active, sort_order) VALUES
        (:id1, 'regular', 'Regular', 0.0, 0.0, true, 1),
        (:id2, 'vip', 'VIP', 5.0, 10000.0, true, 2),
        (:id3, 'corporate', 'Corporate', 10.0, 50000.0, true, 3),
        (:id4, 'insurance', 'Insurance', 0.0, 100000.0, true, 4),
        (:id5, 'senior', 'Senior Citizen', 5.0, 5000.0, true, 5)
    """), {
        'id1': generate_uuid(), 'id2': generate_uuid(), 'id3': generate_uuid(),
        'id4': generate_uuid(), 'id5': generate_uuid()
    })

    # Seed Medicine Types
    conn.execute(text("""
        INSERT INTO medicine_type_master (id, code, name, description, is_active, sort_order) VALUES
        (:id1, 'tablet', 'Tablet', 'Solid oral dosage form', true, 1),
        (:id2, 'capsule', 'Capsule', 'Gelatin-enclosed powder/liquid', true, 2),
        (:id3, 'syrup', 'Syrup', 'Liquid oral solution', true, 3),
        (:id4, 'injection', 'Injection', 'Injectable solution', true, 4),
        (:id5, 'cream', 'Cream/Ointment', 'Topical application', true, 5),
        (:id6, 'drops', 'Drops', 'Eye/Ear/Nasal drops', true, 6),
        (:id7, 'powder', 'Powder', 'Powder for reconstitution', true, 7),
        (:id8, 'inhaler', 'Inhaler', 'Respiratory inhaler', true, 8),
        (:id9, 'patch', 'Transdermal Patch', 'Skin adhesive patch', true, 9),
        (:id10, 'suppository', 'Suppository', 'Rectal/Vaginal insert', true, 10),
        (:id11, 'gel', 'Gel', 'Topical gel', true, 11),
        (:id12, 'spray', 'Spray', 'Nasal/Oral spray', true, 12),
        (:id13, 'suspension', 'Suspension', 'Liquid with suspended particles', true, 13),
        (:id14, 'other', 'Other', 'Other dosage forms', true, 99)
    """), {
        'id1': generate_uuid(), 'id2': generate_uuid(), 'id3': generate_uuid(),
        'id4': generate_uuid(), 'id5': generate_uuid(), 'id6': generate_uuid(),
        'id7': generate_uuid(), 'id8': generate_uuid(), 'id9': generate_uuid(),
        'id10': generate_uuid(), 'id11': generate_uuid(), 'id12': generate_uuid(),
        'id13': generate_uuid(), 'id14': generate_uuid()
    })

    # Seed GST Slabs
    conn.execute(text("""
        INSERT INTO gst_slab_master (id, rate, cgst_rate, sgst_rate, igst_rate, description, is_active) VALUES
        (:id1, 0.0, 0.0, 0.0, 0.0, 'Exempt - Essential Medicines', true),
        (:id2, 5.0, 2.5, 2.5, 5.0, 'Lower Rate - Common Drugs', true),
        (:id3, 12.0, 6.0, 6.0, 12.0, 'Standard Rate - Most Medicines', true),
        (:id4, 18.0, 9.0, 9.0, 18.0, 'Higher Rate - Premium Products', true),
        (:id5, 28.0, 14.0, 14.0, 28.0, 'Highest Rate - Luxury Items', true)
    """), {
        'id1': generate_uuid(), 'id2': generate_uuid(), 'id3': generate_uuid(),
        'id4': generate_uuid(), 'id5': generate_uuid()
    })

    # Seed Genders
    conn.execute(text("""
        INSERT INTO gender_master (id, code, name, is_active, sort_order) VALUES
        (:id1, 'male', 'Male', true, 1),
        (:id2, 'female', 'Female', true, 2),
        (:id3, 'other', 'Other', true, 3),
        (:id4, 'prefer_not', 'Prefer not to say', true, 4)
    """), {
        'id1': generate_uuid(), 'id2': generate_uuid(),
        'id3': generate_uuid(), 'id4': generate_uuid()
    })

    # Seed Employment Types
    conn.execute(text("""
        INSERT INTO employment_type_master (id, code, name, description, is_active, sort_order) VALUES
        (:id1, 'full_time', 'Full-Time', 'Regular full-time employee', true, 1),
        (:id2, 'part_time', 'Part-Time', 'Part-time employee', true, 2),
        (:id3, 'contract', 'Contract', 'Fixed-term contract', true, 3),
        (:id4, 'intern', 'Intern', 'Internship position', true, 4),
        (:id5, 'consultant', 'Consultant', 'External consultant', true, 5)
    """), {
        'id1': generate_uuid(), 'id2': generate_uuid(), 'id3': generate_uuid(),
        'id4': generate_uuid(), 'id5': generate_uuid()
    })

    # Seed Urgency Levels
    conn.execute(text("""
        INSERT INTO urgency_master (id, code, name, color, is_active, sort_order) VALUES
        (:id1, 'low', 'Low', 'green', true, 1),
        (:id2, 'normal', 'Normal', 'blue', true, 2),
        (:id3, 'high', 'High', 'orange', true, 3),
        (:id4, 'critical', 'Critical', 'red', true, 4)
    """), {
        'id1': generate_uuid(), 'id2': generate_uuid(),
        'id3': generate_uuid(), 'id4': generate_uuid()
    })

    # Seed Status Master - Invoice statuses
    conn.execute(text("""
        INSERT INTO status_master (id, entity_type, code, name, color, is_terminal, is_default, is_active, sort_order) VALUES
        (:id1, 'invoice', 'draft', 'Draft', 'gray', false, true, true, 1),
        (:id2, 'invoice', 'completed', 'Completed', 'green', true, false, true, 2),
        (:id3, 'invoice', 'cancelled', 'Cancelled', 'red', true, false, true, 3),
        (:id4, 'invoice', 'returned', 'Returned', 'orange', true, false, true, 4)
    """), {
        'id1': generate_uuid(), 'id2': generate_uuid(),
        'id3': generate_uuid(), 'id4': generate_uuid()
    })

    # Seed Status Master - Dispatch statuses
    conn.execute(text("""
        INSERT INTO status_master (id, entity_type, code, name, color, is_terminal, is_default, is_active, sort_order) VALUES
        (:id1, 'dispatch', 'created', 'Created', 'gray', false, true, true, 1),
        (:id2, 'dispatch', 'packed', 'Packed', 'blue', false, false, true, 2),
        (:id3, 'dispatch', 'dispatched', 'Dispatched', 'purple', false, false, true, 3),
        (:id4, 'dispatch', 'in_transit', 'In Transit', 'orange', false, false, true, 4),
        (:id5, 'dispatch', 'delivered', 'Delivered', 'green', true, false, true, 5),
        (:id6, 'dispatch', 'cancelled', 'Cancelled', 'red', true, false, true, 6)
    """), {
        'id1': generate_uuid(), 'id2': generate_uuid(), 'id3': generate_uuid(),
        'id4': generate_uuid(), 'id5': generate_uuid(), 'id6': generate_uuid()
    })

    # Seed Status Master - Purchase Request statuses
    conn.execute(text("""
        INSERT INTO status_master (id, entity_type, code, name, color, is_terminal, is_default, is_active, sort_order) VALUES
        (:id1, 'purchase_request', 'pending', 'Pending', 'yellow', false, true, true, 1),
        (:id2, 'purchase_request', 'approved', 'Approved', 'blue', false, false, true, 2),
        (:id3, 'purchase_request', 'partial', 'Partially Fulfilled', 'purple', false, false, true, 3),
        (:id4, 'purchase_request', 'rejected', 'Rejected', 'red', true, false, true, 4),
        (:id5, 'purchase_request', 'completed', 'Completed', 'green', true, false, true, 5)
    """), {
        'id1': generate_uuid(), 'id2': generate_uuid(), 'id3': generate_uuid(),
        'id4': generate_uuid(), 'id5': generate_uuid()
    })

    # Seed Designations
    conn.execute(text("""
        INSERT INTO designation_master (id, code, name, level, is_active, sort_order) VALUES
        (:id1, 'pharmacist', 'Pharmacist', 3, true, 1),
        (:id2, 'senior_pharmacist', 'Senior Pharmacist', 4, true, 2),
        (:id3, 'pharmacy_manager', 'Pharmacy Manager', 5, true, 3),
        (:id4, 'cashier', 'Cashier', 2, true, 4),
        (:id5, 'sales_rep', 'Sales Representative', 2, true, 5),
        (:id6, 'delivery_boy', 'Delivery Boy', 1, true, 6),
        (:id7, 'store_keeper', 'Store Keeper', 2, true, 7),
        (:id8, 'accountant', 'Accountant', 3, true, 8),
        (:id9, 'hr_manager', 'HR Manager', 4, true, 9),
        (:id10, 'admin', 'Administrator', 5, true, 10)
    """), {
        'id1': generate_uuid(), 'id2': generate_uuid(), 'id3': generate_uuid(),
        'id4': generate_uuid(), 'id5': generate_uuid(), 'id6': generate_uuid(),
        'id7': generate_uuid(), 'id8': generate_uuid(), 'id9': generate_uuid(),
        'id10': generate_uuid()
    })

    # Seed Departments
    conn.execute(text("""
        INSERT INTO department_master (id, code, name, description, is_active, sort_order) VALUES
        (:id1, 'pharmacy', 'Pharmacy', 'Dispensing and customer service', true, 1),
        (:id2, 'sales', 'Sales', 'Sales and marketing', true, 2),
        (:id3, 'inventory', 'Inventory', 'Stock management', true, 3),
        (:id4, 'accounts', 'Accounts', 'Finance and accounting', true, 4),
        (:id5, 'hr', 'Human Resources', 'HR and administration', true, 5),
        (:id6, 'logistics', 'Logistics', 'Delivery and dispatch', true, 6),
        (:id7, 'it', 'IT', 'Technology support', true, 7),
        (:id8, 'management', 'Management', 'Senior management', true, 8)
    """), {
        'id1': generate_uuid(), 'id2': generate_uuid(), 'id3': generate_uuid(),
        'id4': generate_uuid(), 'id5': generate_uuid(), 'id6': generate_uuid(),
        'id7': generate_uuid(), 'id8': generate_uuid()
    })


def downgrade():
    op.drop_table('department_master')
    op.drop_table('designation_master')
    op.drop_index('idx_status_entity', 'status_master')
    op.drop_table('status_master')
    op.drop_table('urgency_master')
    op.drop_table('employment_type_master')
    op.drop_table('gender_master')
    op.drop_table('gst_slab_master')
    op.drop_table('medicine_type_master')
    op.drop_table('customer_type_master')
    op.drop_table('shop_type_master')
    op.drop_table('payment_method_master')
