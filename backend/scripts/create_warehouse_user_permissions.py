"""
Create warehouse-scoped user management permissions
"""
# -*- coding: utf-8 -*-
import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Permission

def create_warehouse_user_permissions():
    db: Session = SessionLocal()
    
    try:
        permissions_to_create = [
            {
                "code": "users.view.warehouse",
                "module": "users",
                "action": "view",
                "scope": "warehouse",
                "description": "View users in assigned warehouse"
            },
            {
                "code": "users.create.warehouse",
                "module": "users",
                "action": "create",
                "scope": "warehouse",
                "description": "Create users for assigned warehouse"
            },
            {
                "code": "users.update.warehouse",
                "module": "users",
                "action": "update",
                "scope": "warehouse",
                "description": "Update users in assigned warehouse"
            },
            {
                "code": "users.delete.warehouse",
                "module": "users",
                "action": "delete",
                "scope": "warehouse",
                "description": "Deactivate users in assigned warehouse"
            },
        ]
        
        created_count = 0
        existing_count = 0
        
        for perm_data in permissions_to_create:
            # Check if permission already exists
            existing = db.query(Permission).filter(Permission.code == perm_data["code"]).first()
            
            if existing:
                print(f"⏭️  Already exists: {perm_data['code']}")
                existing_count += 1
            else:
                # Create new permission
                permission = Permission(**perm_data)
                db.add(permission)
                print(f"✅ Created: {perm_data['code']}")
                created_count += 1
        
        db.commit()
        
        print(f"\n{'='*60}")
        print(f"✅ Created {created_count} new permissions")
        print(f"⏭️  {existing_count} already existed")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Creating Warehouse-Scoped User Permissions...")
    print("="*60)
    create_warehouse_user_permissions()
