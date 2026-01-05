"""
Database Seed Script - Create sample data for all modules
Run with: python -m scripts.seed_data
"""
import sys
sys.path.insert(0, '.')

from datetime import datetime, date, timedelta
from app.db.database import SessionLocal, engine
from app.db.models import (
    User, Role, Warehouse, MedicalShop, Medicine, Batch, Customer,
    Employee, PurchaseRequest, PurchaseRequestItem, Dispatch, DispatchItem,
    Notification, Setting, WarehouseStock, ShopStock,
    RoleType, WarehouseStatus, ShopStatus, MedicineType
)
from app.core.security import get_password_hash


def seed_database():
    db = SessionLocal()
    
    try:
        print("🌱 Starting database seed...")
        
        # ==================== 1. USERS & ROLES ====================
        print("  Creating users...")
        
        admin = User(
            email="admin@pharmaec.com",
            password_hash=get_password_hash("admin123"),
            full_name="Super Administrator",
            phone="+91-9876543210",
            role=RoleType.SUPER_ADMIN,
            is_active=True
        )
        db.add(admin)
        
        warehouse_admin = User(
            email="warehouse@pharmaec.com",
            password_hash=get_password_hash("warehouse123"),
            full_name="Warehouse Manager",
            phone="+91-9876543211",
            role=RoleType.WAREHOUSE_ADMIN,
            is_active=True
        )
        db.add(warehouse_admin)
        
        shop_owner = User(
            email="shop@pharmaec.com",
            password_hash=get_password_hash("shop123"),
            full_name="Shop Owner",
            phone="+91-9876543212",
            role=RoleType.SHOP_OWNER,
            is_active=True
        )
        db.add(shop_owner)
        
        pharmacist = User(
            email="pharmacist@pharmaec.com",
            password_hash=get_password_hash("pharmacist123"),
            full_name="John Pharmacist",
            phone="+91-9876543213",
            role=RoleType.PHARMACIST,
            is_active=True
        )
        db.add(pharmacist)
        
        db.flush()
        
        # ==================== 2. ROLES ====================
        print("  Creating roles...")
        
        roles_data = [
            ("Super Admin", "Full system access", "*"),
            ("Warehouse Admin", "Warehouse management access", "warehouse:*,dispatch:*,inventory:*"),
            ("Shop Owner", "Shop management and sales", "shop:*,sales:*,purchase:*"),
            ("Pharmacist", "POS and customer service", "pos:*,customer:*"),
            ("Cashier", "POS billing only", "pos:billing"),
            ("HR Manager", "Employee and payroll", "hr:*,employee:*"),
        ]
        
        for name, desc, perms in roles_data:
            role = Role(name=name, description=desc, permissions=perms, is_system=True)
            db.add(role)
        
        db.flush()
        
        # ==================== 3. WAREHOUSES ====================
        print("  Creating warehouses...")
        
        warehouse1 = Warehouse(
            name="Central Distribution Center",
            code="WH-CDC-001",
            address="123 Industrial Area, Phase 1",
            city="Mumbai",
            state="Maharashtra",
            pincode="400001",
            phone="+91-22-12345678",
            email="cdc@pharmaec.com",
            manager_id=warehouse_admin.id,
            capacity=10000,
            status=WarehouseStatus.ACTIVE
        )
        db.add(warehouse1)
        
        warehouse2 = Warehouse(
            name="North Region Warehouse",
            code="WH-NRW-002",
            address="456 MIDC Area",
            city="Pune",
            state="Maharashtra",
            pincode="411001",
            phone="+91-20-87654321",
            email="nrw@pharmaec.com",
            capacity=5000,
            status=WarehouseStatus.ACTIVE
        )
        db.add(warehouse2)
        
        db.flush()
        
        # ==================== 4. MEDICAL SHOPS ====================
        print("  Creating medical shops...")
        
        shop1 = MedicalShop(
            name="HealthPlus Pharmacy - Andheri",
            code="SH-HP-001",
            shop_type="retail",
            license_number="DL-MH-2024-001234",
            gst_number="27AAACH1234A1ZV",
            address="Shop 101, Commercial Complex",
            city="Mumbai",
            state="Maharashtra",
            pincode="400069",
            phone="+91-22-23456789",
            email="andheri@healthplus.com",
            owner_id=shop_owner.id,
            warehouse_id=warehouse1.id,
            status=ShopStatus.ACTIVE
        )
        db.add(shop1)
        
        shop2 = MedicalShop(
            name="MediCare Pharmacy - Bandra",
            code="SH-MC-002",
            shop_type="retail",
            license_number="DL-MH-2024-001235",
            gst_number="27AAACH1234A1ZW",
            address="Shop 205, Main Road",
            city="Mumbai",
            state="Maharashtra",
            pincode="400050",
            phone="+91-22-34567890",
            email="bandra@medicare.com",
            warehouse_id=warehouse1.id,
            status=ShopStatus.ACTIVE
        )
        db.add(shop2)
        
        shop3 = MedicalShop(
            name="Wellness Pharmacy - Pune",
            code="SH-WP-003",
            shop_type="retail",
            license_number="DL-MH-2024-001236",
            address="Shop 10, FC Road",
            city="Pune",
            state="Maharashtra",
            pincode="411001",
            phone="+91-20-45678901",
            warehouse_id=warehouse2.id,
            status=ShopStatus.ACTIVE
        )
        db.add(shop3)
        
        db.flush()
        
        # ==================== 5. MEDICINES ====================
        print("  Creating medicines...")
        
        medicines_data = [
            ("Amoxicillin 500mg", "Amoxicillin", "Cipla", MedicineType.CAPSULE, "antibiotics", 125.00, 85.00),
            ("Paracetamol 650mg", "Paracetamol", "GSK", MedicineType.TABLET, "painkillers", 35.00, 20.00),
            ("Azithromycin 500mg", "Azithromycin", "Zydus", MedicineType.TABLET, "antibiotics", 180.00, 120.00),
            ("Metformin 500mg", "Metformin HCL", "Sun Pharma", MedicineType.TABLET, "diabetes", 45.00, 28.00),
            ("Omeprazole 20mg", "Omeprazole", "Dr. Reddy's", MedicineType.CAPSULE, "gastrointestinal", 95.00, 60.00),
            ("Cetirizine 10mg", "Cetirizine", "Cipla", MedicineType.TABLET, "antiallergy", 25.00, 15.00),
            ("Atorvastatin 10mg", "Atorvastatin", "Ranbaxy", MedicineType.TABLET, "cardiac", 150.00, 95.00),
            ("Ibuprofen 400mg", "Ibuprofen", "Abbott", MedicineType.TABLET, "painkillers", 55.00, 35.00),
            ("Amlodipine 5mg", "Amlodipine", "Torrent", MedicineType.TABLET, "cardiac", 65.00, 40.00),
            ("Vitamin D3 1000IU", "Cholecalciferol", "Mankind", MedicineType.CAPSULE, "vitamins", 280.00, 180.00),
            ("Cough Syrup", "Dextromethorphan", "Dabur", MedicineType.SYRUP, "cough", 120.00, 75.00),
            ("Eye Drops", "Ofloxacin", "Alcon", MedicineType.DROPS, "ophthalmic", 85.00, 55.00),
        ]
        
        medicines = []
        for name, generic, mfr, med_type, category, mrp, pp in medicines_data:
            med = Medicine(
                name=name,
                generic_name=generic,
                manufacturer=mfr,
                medicine_type=med_type,
                category=category,
                mrp=mrp,
                purchase_price=pp,
                gst_rate=12.0,
                pack_size=10,
                reorder_level=50,
                is_active=True
            )
            db.add(med)
            medicines.append(med)
        
        db.flush()
        
        # ==================== 6. BATCHES & STOCK ====================
        print("  Creating batches and stock...")
        
        today = date.today()
        batches = []
        
        for i, med in enumerate(medicines):
            # Create 2 batches per medicine
            for j in range(2):
                expiry_months = 12 + (j * 6) + (i % 6)
                qty = 100 + (i * 10) + (j * 50)
                
                batch = Batch(
                    medicine_id=med.id,
                    batch_number=f"B{today.year}{i+1:02d}{j+1}",
                    manufacturing_date=today - timedelta(days=30),
                    expiry_date=today + timedelta(days=expiry_months * 30),
                    quantity=qty,
                    purchase_price=med.purchase_price,
                    mrp=med.mrp,
                    supplier="ABC Distributors"
                )
                db.add(batch)
                batches.append(batch)
        
        db.flush()
        
        # Add warehouse stock
        for batch in batches:
            wh_stock = WarehouseStock(
                warehouse_id=warehouse1.id,
                medicine_id=batch.medicine_id,
                batch_id=batch.id,
                quantity=batch.quantity
            )
            db.add(wh_stock)
        
        # Add some shop stock
        for i, batch in enumerate(batches[:10]):
            shop_stock = ShopStock(
                shop_id=shop1.id,
                medicine_id=batch.medicine_id,
                batch_id=batch.id,
                quantity=int(batch.quantity * 0.3)
            )
            db.add(shop_stock)
        
        db.flush()
        
        # ==================== 7. CUSTOMERS ====================
        print("  Creating customers...")
        
        customers_data = [
            ("Rahul Sharma", "+91-9812345670", "rahul@email.com", "Mumbai"),
            ("Priya Patel", "+91-9812345671", "priya@email.com", "Mumbai"),
            ("Amit Singh", "+91-9812345672", "amit@email.com", "Pune"),
            ("Deepika Nair", "+91-9812345673", "deepika@email.com", "Mumbai"),
            ("Vikram Reddy", "+91-9812345674", "vikram@email.com", "Pune"),
        ]
        
        for name, phone, email, city in customers_data:
            customer = Customer(
                name=name,
                phone=phone,
                email=email,
                city=city,
                customer_type="regular",
                shop_id=shop1.id
            )
            db.add(customer)
        
        db.flush()
        
        # ==================== 8. EMPLOYEES ====================
        print("  Creating employees...")
        
        employees_data = [
            ("EMP-001", "Rajesh Kumar", "rajesh@pharmaec.com", "+91-9898989801", "Pharmacist", "Dispensary", 45000),
            ("EMP-002", "Sneha Gupta", "sneha@pharmaec.com", "+91-9898989802", "Cashier", "Billing", 25000),
            ("EMP-003", "Vikrant Shah", "vikrant@pharmaec.com", "+91-9898989803", "Store Manager", "Operations", 55000),
        ]
        
        for code, name, email, phone, desig, dept, salary in employees_data:
            emp = Employee(
                employee_code=code,
                name=name,
                email=email,
                phone=phone,
                designation=desig,
                department=dept,
                employment_type="full_time",
                date_of_joining=today - timedelta(days=365),
                basic_salary=salary,
                shop_id=shop1.id,
                status="active"
            )
            db.add(emp)
        
        db.flush()
        
        # ==================== 9. SETTINGS ====================
        print("  Creating settings...")
        
        settings_data = [
            ("company_name", "PharmaEC Enterprises", "Company name", "general"),
            ("currency", "INR", "Default currency", "general"),
            ("timezone", "Asia/Kolkata", "Default timezone", "general"),
            ("gst_rate", "12", "Default GST rate", "tax"),
            ("cgst_rate", "6", "CGST rate", "tax"),
            ("sgst_rate", "6", "SGST rate", "tax"),
            ("low_stock_threshold", "50", "Low stock alert threshold", "inventory"),
            ("expiry_alert_days", "90", "Days before expiry alert", "inventory"),
        ]
        
        for key, value, desc, category in settings_data:
            setting = Setting(key=key, value=value, description=desc, category=category)
            db.add(setting)
        
        # ==================== 10. NOTIFICATIONS ====================
        print("  Creating sample notifications...")
        
        notification = Notification(
            type="system",
            title="Welcome to PharmaEC",
            message="Your pharmacy management system is now ready to use.",
            priority="high",
            user_id=admin.id
        )
        db.add(notification)
        
        notification2 = Notification(
            type="low_stock",
            title="Low Stock Alert",
            message="Paracetamol 650mg is running low. Current stock: 45 units.",
            priority="medium",
            shop_id=shop1.id
        )
        db.add(notification2)
        
        db.commit()
        
        print("✅ Database seeded successfully!")
        print(f"""
Summary:
  - Users: 4 (admin, warehouse, shop, pharmacist)
  - Roles: 6
  - Warehouses: 2
  - Medical Shops: 3
  - Medicines: {len(medicines)}
  - Batches: {len(batches)}
  - Customers: 5
  - Employees: 3
  - Settings: 8

Login Credentials:
  Admin: admin@pharmaec.com / admin123
  Warehouse: warehouse@pharmaec.com / warehouse123
  Shop: shop@pharmaec.com / shop123
  Pharmacist: pharmacist@pharmaec.com / pharmacist123
        """)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
