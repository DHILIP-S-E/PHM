import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import User, Warehouse

def fix_admin_and_test():
    db = SessionLocal()
    try:
        # Find Warehouse Admin
        admin = db.query(User).filter(User.email == "test.whadmin@phm.test").first()
        if not admin:
            print("❌ Admin user not found")
            return

        print(f"Admin Found: {admin.email}")
        print(f"Current Warehouse ID: {admin.assigned_warehouse_id}")
        
        # Ensure a warehouse exists
        warehouse = db.query(Warehouse).first()
        if not warehouse:
            print("❌ No warehouses in DB!")
            return
            
        print(f"Using Warehouse: {warehouse.name} ({warehouse.id})")
        
        # Fix Admin Assignment if missing
        if not admin.assigned_warehouse_id:
            print("⚠️ Admin has no warehouse! Fixing...")
            admin.assigned_warehouse_id = warehouse.id
            db.commit()
            print("✅ Admin assigned to warehouse.")
        
        # Now Run the Test Logic here directly
        from app.api.v1.employees import create_employee
        from app.models.employee import EmployeeCreate
        from app.core.security import AuthContext
        
        auth = AuthContext(
            user_id=admin.id,
            email=admin.email,
            role="warehouse_admin",
            warehouse_id=admin.assigned_warehouse_id,
            shop_id=None
        )
        
        emp_data = EmployeeCreate(
            name="Auto Test Worker",
            email=f"autoworker.{admin.assigned_warehouse_id[:4]}@test.local",
            phone="9988001122",
            designation="Helper",
            department="Ops",
            employment_type="full_time",
            date_of_joining="2024-01-01",
            date_of_birth="1990-01-01",
            gender="male",
            basic_salary=12000,
            password="Pass123"
        )
        
        # Check if user already exists
        exist = db.query(User).filter(User.email == emp_data.email).first()
        if exist:
            print("User already exists, deleting for retry...")
            db.delete(exist)
            db.commit()
            
        print("Creating Employee via API function...")
        try:
            resp = create_employee(emp_data, db, auth)
            print(f"✅ Created: {resp.message}")
            
            # Verify User
            new_user = db.query(User).filter(User.email == emp_data.email).first()
            if new_user:
                 print(f"   User Role: {new_user.role}")
                 print(f"   User WH ID: {new_user.assigned_warehouse_id}")
                 
                 if new_user.assigned_warehouse_id == admin.assigned_warehouse_id:
                     print("   ✅ SUCCESS: User is linked to correct warehouse")
                 else:
                     print("   ❌ FAILURE: IDs do not match")
            else:
                print("   ❌ FAILURE: User record not created")
                
        except Exception as e:
            print(f"❌ Creation Failed: {e}")
            import traceback
            traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    fix_admin_and_test()
