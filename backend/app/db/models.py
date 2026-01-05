"""
SQLAlchemy ORM Models for PharmaEC Management System - Complete Production Version
"""
from datetime import datetime, date
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Date, Text, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid
import enum


def generate_uuid():
    return str(uuid.uuid4())


# ==================== ENUMS ====================

class RoleType(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    WAREHOUSE_ADMIN = "warehouse_admin"
    SHOP_OWNER = "shop_owner"
    PHARMACIST = "pharmacist"
    CASHIER = "cashier"
    HR_MANAGER = "hr_manager"
    ACCOUNTANT = "accountant"


class WarehouseStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


class ShopStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class MedicineType(str, enum.Enum):
    TABLET = "tablet"
    CAPSULE = "capsule"
    SYRUP = "syrup"
    INJECTION = "injection"
    CREAM = "cream"
    OINTMENT = "ointment"
    DROPS = "drops"
    POWDER = "powder"
    OTHER = "other"


class MovementType(str, enum.Enum):
    IN = "in"
    OUT = "out"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"


class InvoiceStatus(str, enum.Enum):
    DRAFT = "draft"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RETURNED = "returned"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PARTIAL = "partial"
    COMPLETED = "completed"
    REFUNDED = "refunded"


class PurchaseRequestStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    PARTIAL = "partial"
    REJECTED = "rejected"
    COMPLETED = "completed"


class DispatchStatus(str, enum.Enum):
    CREATED = "created"
    PACKED = "packed"
    DISPATCHED = "dispatched"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class AttendanceStatus(str, enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    LEAVE = "leave"


# ==================== AUTH MODELS ====================

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    role = Column(SQLEnum(RoleType), default=RoleType.PHARMACIST)
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")


class Role(Base):
    __tablename__ = "roles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    permissions = Column(Text)  # JSON string of permissions
    is_system = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(String(36), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    refresh_token = Column(String(500), nullable=False)
    device_info = Column(String(255))
    ip_address = Column(String(45))
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sessions")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class LoginAuditLog(Base):
    __tablename__ = "login_audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"))
    email = Column(String(255), nullable=False)
    action = Column(String(50), nullable=False)  # login_success, login_failed, logout
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)


# ==================== ORGANIZATION MODELS ====================

class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    address = Column(Text, nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    country = Column(String(50), default="India")
    pincode = Column(String(10), nullable=False)
    phone = Column(String(20))
    email = Column(String(255))
    manager_id = Column(String(36), ForeignKey("users.id"))
    capacity = Column(Integer)
    status = Column(SQLEnum(WarehouseStatus), default=WarehouseStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    shops = relationship("MedicalShop", back_populates="warehouse")
    stock = relationship("WarehouseStock", back_populates="warehouse")


class MedicalShop(Base):
    __tablename__ = "medical_shops"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    shop_type = Column(String(20), default="retail")
    license_number = Column(String(50), nullable=False)
    license_expiry = Column(Date)
    gst_number = Column(String(20))
    address = Column(Text, nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    country = Column(String(50), default="India")
    pincode = Column(String(10), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255))
    owner_id = Column(String(36), ForeignKey("users.id"))
    manager_id = Column(String(36), ForeignKey("users.id"))
    warehouse_id = Column(String(36), ForeignKey("warehouses.id"))
    status = Column(SQLEnum(ShopStatus), default=ShopStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    warehouse = relationship("Warehouse", back_populates="shops")
    stock = relationship("ShopStock", back_populates="shop")


# ==================== MEDICINE MODELS ====================

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False, index=True)
    generic_name = Column(String(200), nullable=False)
    brand = Column(String(100))
    manufacturer = Column(String(200), nullable=False)
    medicine_type = Column(SQLEnum(MedicineType), default=MedicineType.TABLET)
    category = Column(String(50))
    composition = Column(Text)
    strength = Column(String(50))
    unit = Column(String(20), default="strip")
    pack_size = Column(Integer, default=10)
    hsn_code = Column(String(20))
    gst_rate = Column(Float, default=12.0)
    mrp = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    is_prescription_required = Column(Boolean, default=False)
    is_controlled = Column(Boolean, default=False)
    storage_conditions = Column(Text)
    reorder_level = Column(Integer, default=50)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    batches = relationship("Batch", back_populates="medicine")


class Batch(Base):
    __tablename__ = "batches"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    medicine_id = Column(String(36), ForeignKey("medicines.id"), nullable=False)
    batch_number = Column(String(50), nullable=False, index=True)
    manufacturing_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=False, index=True)
    quantity = Column(Integer, default=0)
    purchase_price = Column(Float, nullable=False)
    mrp = Column(Float, nullable=False)
    supplier = Column(String(200))
    received_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)

    medicine = relationship("Medicine", back_populates="batches")

    __table_args__ = (Index('idx_batch_expiry', 'expiry_date'),)


# ==================== STOCK MODELS (CRITICAL) ====================

class WarehouseStock(Base):
    """Stock quantity per medicine/batch at warehouse level"""
    __tablename__ = "warehouse_stock"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    warehouse_id = Column(String(36), ForeignKey("warehouses.id"), nullable=False)
    medicine_id = Column(String(36), ForeignKey("medicines.id"), nullable=False)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    reserved_quantity = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    warehouse = relationship("Warehouse", back_populates="stock")

    __table_args__ = (
        Index('idx_wh_stock_lookup', 'warehouse_id', 'medicine_id', 'batch_id'),
    )


class ShopStock(Base):
    """Stock quantity per medicine/batch at shop level"""
    __tablename__ = "shop_stock"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    shop_id = Column(String(36), ForeignKey("medical_shops.id"), nullable=False)
    medicine_id = Column(String(36), ForeignKey("medicines.id"), nullable=False)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    reserved_quantity = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shop = relationship("MedicalShop", back_populates="stock")

    __table_args__ = (
        Index('idx_shop_stock_lookup', 'shop_id', 'medicine_id', 'batch_id'),
    )


class StockMovement(Base):
    """ALL stock changes MUST go through this table"""
    __tablename__ = "stock_movements"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    movement_type = Column(SQLEnum(MovementType), nullable=False)
    
    # Source location
    source_type = Column(String(20))  # warehouse, shop, supplier
    source_id = Column(String(36))
    
    # Destination location
    destination_type = Column(String(20))  # warehouse, shop, customer
    destination_id = Column(String(36))
    
    # Item details
    medicine_id = Column(String(36), ForeignKey("medicines.id"), nullable=False)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    # Reference
    reference_type = Column(String(50))  # purchase, sale, dispatch, adjustment, return
    reference_id = Column(String(36))
    
    # Audit
    notes = Column(Text)
    created_by = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_movement_ref', 'reference_type', 'reference_id'),
        Index('idx_movement_date', 'created_at'),
    )


# ==================== INVOICE & BILLING MODELS ====================

class Customer(Base):
    __tablename__ = "customers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False, index=True)
    email = Column(String(255))
    date_of_birth = Column(Date)
    gender = Column(String(10))
    address = Column(Text)
    city = Column(String(50))
    pincode = Column(String(10))
    customer_type = Column(String(20), default="regular")
    shop_id = Column(String(36), ForeignKey("medical_shops.id"))
    total_purchases = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    loyalty_points = Column(Integer, default=0)
    last_visit = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    shop_id = Column(String(36), ForeignKey("medical_shops.id"), nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id"))
    payment_method = Column(String(20), default="cash")
    subtotal = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    discount_percent = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    paid_amount = Column(Float, default=0.0)
    balance_amount = Column(Float, default=0.0)
    status = Column(SQLEnum(InvoiceStatus), default=InvoiceStatus.COMPLETED)
    payment_status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.COMPLETED)
    billed_by = Column(String(36), ForeignKey("users.id"))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    invoice_id = Column(String(36), ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    medicine_id = Column(String(36), ForeignKey("medicines.id"), nullable=False)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    discount_percent = Column(Float, default=0.0)
    tax_percent = Column(Float, default=12.0)
    subtotal = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    total = Column(Float, default=0.0)

    invoice = relationship("Invoice", back_populates="items")


class Return(Base):
    __tablename__ = "returns"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    return_number = Column(String(50), unique=True, nullable=False)
    invoice_id = Column(String(36), ForeignKey("invoices.id"), nullable=False)
    shop_id = Column(String(36), ForeignKey("medical_shops.id"), nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id"))
    total_refund = Column(Float, default=0.0)
    refund_method = Column(String(20), default="cash")
    reason = Column(Text)
    processed_by = Column(String(36), ForeignKey("users.id"))
    status = Column(String(20), default="completed")
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("ReturnItem", back_populates="return_record", cascade="all, delete-orphan")


class ReturnItem(Base):
    __tablename__ = "return_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    return_id = Column(String(36), ForeignKey("returns.id", ondelete="CASCADE"), nullable=False)
    invoice_item_id = Column(String(36), ForeignKey("invoice_items.id"))
    medicine_id = Column(String(36), ForeignKey("medicines.id"), nullable=False)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    refund_amount = Column(Float, nullable=False)
    reason = Column(Text)

    return_record = relationship("Return", back_populates="items")


# ==================== PURCHASE & DISPATCH MODELS ====================

class PurchaseRequest(Base):
    __tablename__ = "purchase_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    request_number = Column(String(50), unique=True, nullable=False, index=True)
    shop_id = Column(String(36), ForeignKey("medical_shops.id"), nullable=False)
    warehouse_id = Column(String(36), ForeignKey("warehouses.id"), nullable=False)
    urgency = Column(String(20), default="normal")
    status = Column(SQLEnum(PurchaseRequestStatus), default=PurchaseRequestStatus.PENDING)
    requested_by = Column(String(36), ForeignKey("users.id"))
    approved_by = Column(String(36), ForeignKey("users.id"))
    approval_notes = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

    items = relationship("PurchaseRequestItem", back_populates="purchase_request", cascade="all, delete-orphan")


class PurchaseRequestItem(Base):
    __tablename__ = "purchase_request_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    purchase_request_id = Column(String(36), ForeignKey("purchase_requests.id", ondelete="CASCADE"), nullable=False)
    medicine_id = Column(String(36), ForeignKey("medicines.id"), nullable=False)
    quantity_requested = Column(Integer, nullable=False)
    quantity_approved = Column(Integer, default=0)
    quantity_dispatched = Column(Integer, default=0)
    notes = Column(Text)

    purchase_request = relationship("PurchaseRequest", back_populates="items")


class Dispatch(Base):
    __tablename__ = "dispatches"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    dispatch_number = Column(String(50), unique=True, nullable=False, index=True)
    warehouse_id = Column(String(36), ForeignKey("warehouses.id"), nullable=False)
    shop_id = Column(String(36), ForeignKey("medical_shops.id"), nullable=False)
    purchase_request_id = Column(String(36), ForeignKey("purchase_requests.id"))
    status = Column(SQLEnum(DispatchStatus), default=DispatchStatus.CREATED)
    dispatched_by = Column(String(36), ForeignKey("users.id"))
    received_by = Column(String(36), ForeignKey("users.id"))
    dispatched_at = Column(DateTime)
    delivered_at = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("DispatchItem", back_populates="dispatch", cascade="all, delete-orphan")
    status_history = relationship("DispatchStatusHistory", back_populates="dispatch", cascade="all, delete-orphan")


class DispatchItem(Base):
    __tablename__ = "dispatch_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    dispatch_id = Column(String(36), ForeignKey("dispatches.id", ondelete="CASCADE"), nullable=False)
    medicine_id = Column(String(36), ForeignKey("medicines.id"), nullable=False)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    dispatch = relationship("Dispatch", back_populates="items")


class DispatchStatusHistory(Base):
    __tablename__ = "dispatch_status_history"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    dispatch_id = Column(String(36), ForeignKey("dispatches.id", ondelete="CASCADE"), nullable=False)
    status = Column(SQLEnum(DispatchStatus), nullable=False)
    notes = Column(Text)
    updated_by = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    dispatch = relationship("Dispatch", back_populates="status_history")


# ==================== HR MODELS ====================

class Employee(Base):
    __tablename__ = "employees"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    employee_code = Column(String(20), unique=True, nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"))
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    designation = Column(String(50), nullable=False)
    department = Column(String(50), nullable=False)
    employment_type = Column(String(20), default="full_time")
    date_of_joining = Column(Date, nullable=False)
    date_of_birth = Column(Date)
    gender = Column(String(10))
    address = Column(Text)
    city = Column(String(50))
    emergency_contact = Column(String(20))
    bank_account = Column(String(50))
    pan_number = Column(String(20))
    pf_number = Column(String(30))
    esi_number = Column(String(30))
    basic_salary = Column(Float, nullable=False)
    shop_id = Column(String(36), ForeignKey("medical_shops.id"))
    warehouse_id = Column(String(36), ForeignKey("warehouses.id"))
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

    attendance_records = relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")
    salary_records = relationship("SalaryRecord", back_populates="employee", cascade="all, delete-orphan")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    employee_id = Column(String(36), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(SQLEnum(AttendanceStatus), default=AttendanceStatus.PRESENT)
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    working_hours = Column(Float, default=0.0)
    overtime_hours = Column(Float, default=0.0)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="attendance_records")

    __table_args__ = (Index('idx_attendance_date', 'employee_id', 'date'),)


class SalaryRecord(Base):
    __tablename__ = "salary_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    employee_id = Column(String(36), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    basic_salary = Column(Float, nullable=False)
    hra = Column(Float, default=0.0)
    allowances = Column(Float, default=0.0)
    deductions = Column(Float, default=0.0)
    pf_deduction = Column(Float, default=0.0)
    esi_deduction = Column(Float, default=0.0)
    tax_deduction = Column(Float, default=0.0)
    bonus = Column(Float, default=0.0)
    gross_salary = Column(Float, nullable=False)
    net_salary = Column(Float, nullable=False)
    is_paid = Column(Boolean, default=False)
    paid_at = Column(DateTime)
    payment_ref = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee", back_populates="salary_records")


# ==================== CRM MODELS ====================

class CustomerFollowup(Base):
    __tablename__ = "customer_followups"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    followup_type = Column(String(50), nullable=False)
    scheduled_date = Column(Date, nullable=False)
    status = Column(String(20), default="pending")
    notes = Column(Text)
    completed_at = Column(DateTime)
    created_by = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


class CustomerPrescription(Base):
    __tablename__ = "customer_prescriptions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    customer_id = Column(String(36), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    doctor_name = Column(String(100))
    hospital = Column(String(200))
    prescription_date = Column(Date)
    notes = Column(Text)
    file_path = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)


# ==================== NOTIFICATION & SETTINGS ====================

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    priority = Column(String(20), default="medium")
    is_read = Column(Boolean, default=False)
    user_id = Column(String(36), ForeignKey("users.id"))
    shop_id = Column(String(36), ForeignKey("medical_shops.id"))
    reference_type = Column(String(50))
    reference_id = Column(String(36))
    created_at = Column(DateTime, default=datetime.utcnow)


class Setting(Base):
    __tablename__ = "settings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(Text)
    category = Column(String(50))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ==================== AUDIT LOG ====================

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"))
    action = Column(String(50), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(36))
    old_values = Column(Text)  # JSON
    new_values = Column(Text)  # JSON
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (Index('idx_audit_entity', 'entity_type', 'entity_id'),)
