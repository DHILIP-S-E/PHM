import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import User, Employee

def check_user_employee():
    db = SessionLocal()
    try:
        print("\n=== Checking war@gmail.com ===\n")
        
        # Check User table
        user = db.query(User).filter(User.email == "war@gmail.com").first()
        if user:
            print(f"✅ User EXISTS:")
            print(f"   Email: {user.email}")
            print(f"   Name: {user.full_name}")
            print(f"   Role: {user.role}")
            print(f"   Warehouse: {user.assigned_warehouse_id}")
            print(f"   Active: {user.is_active}")
        else:
            print("❌ User NOT FOUND in users table")
        
        # Check Employee table
        emp = db.query(Employee).filter(Employee.email == "war@gmail.com").first()
        if emp:
            print(f"\n✅ Employee EXISTS:")
            print(f"   Code: {emp.employee_code}")
            print(f"   Name: {emp.name}")
            print(f"   User ID: {emp.user_id}")
            print(f"   Warehouse: {emp.warehouse_id}")
        else:
            print("\n❌ Employee NOT FOUND in employees table")
            
    finally:
        db.close()

if __name__ == "__main__":
    check_user_employee()
