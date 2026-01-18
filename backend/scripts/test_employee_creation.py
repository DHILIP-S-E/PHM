import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.api.v1.employees import create_employee
from app.models.employee import EmployeeCreate
from app.core.security import AuthContext
from app.db.models import User, RoleType, Role
from datetime import date

def test_warehouse_employee_creation():
    db = SessionLocal()
    try:
        print("\n=== TESTING WAREHOUSE EMPLOYEE CREATION ===\n")
        
        # 1. Get a valid warehouse ID
        admin_user = db.query(User).filter(User.email == "test.whadmin@phm.test").first()
        if not admin_user or not admin_user.assigned_warehouse_id:
             # Fallback
             admin_user = db.query(User).filter(User.role == "warehouse_admin").first()
             
        if not admin_user or not admin_user.assigned_warehouse_id:
            print("❌ No Warehouse Admin found with assigned warehouse. Cannot test.")
            return

        warehouse_id = admin_user.assigned_warehouse_id
        # auth context for Warehouse Admin
        auth_context = AuthContext(
            user_id=admin_user.id,
            role="warehouse_admin",
            warehouse_id=warehouse_id,
            shop_id=None,
            is_super_admin=False
        )
        
        print(f"Simulating Warehouse Admin: {admin_user.email} (Warehouse: {warehouse_id})")
        
        # 2. Prepare Employee Data (Standard Employee)
        emp_data = EmployeeCreate(
            name="Test Warehouse Worker",
            email=f"worker.{warehouse_id[:4]}@test.local",
            phone="9988776655", # distinct phone
            designation="Helper",
            department="Operations",
            employment_type="full_time",
            date_of_joining=date.today(),
            date_of_birth=date(1990, 1, 1),
            gender="male",
            basic_salary=15000,
            password="WorkerPass123!"
        )
        
        # 3. Call create_employee
        print("\nCreating Employee...")
        try:
            response = create_employee(emp_data, db, auth_context)
            print("✅ Employee API Response:", response.message)
        except Exception as e:
            print(f"❌ API Call Failed: {e}")
            import traceback
            traceback.print_exc()
            return

        # 4. Verify in Database
        print("\nVerifying Database Records...")
        
        # Check User Table
        new_user = db.query(User).filter(User.email == emp_data.email).first()
        if new_user:
            print(f"✅ User Created: {new_user.email}")
            print(f"   Role: {new_user.role}")
            print(f"   Assigned Warehouse: {new_user.assigned_warehouse_id}")
            print(f"   Assigned Shop: {new_user.assigned_shop_id}")
            
            if new_user.assigned_warehouse_id == warehouse_id:
                print("   ✅ Warehouse Assignment MATCHES admin's warehouse")
            else:
                print("   ❌ Warehouse Assignment MISMATCH")
                
            if new_user.role in ["warehouse_employee", "employee"]: # Acceptable roles
                 print("   ✅ Role is acceptable")
            else:
                 print(f"   ⚠️ Role '{new_user.role}' might be unexpected")
                 
        else:
            print("❌ User record NOT found!")

        # Check Employee Table
        # (Assuming Employee model is imported safely or query by table)
        from app.db.models import Employee
        new_emp = db.query(Employee).filter(Employee.email == emp_data.email).first()
        if new_emp:
            print(f"✅ Employee Record Created: {new_emp.employee_code}")
            print(f"   Ref User ID: {new_emp.user_id}")
        else:
            print("❌ Employee record NOT found!")
            
    finally:
        db.close()

if __name__ == "__main__":
    test_warehouse_employee_creation()
