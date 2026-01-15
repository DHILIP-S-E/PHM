
"""
Ensure core permissions exist and are assigned to Warehouse Admin
Run with: python -m scripts.ensure_core_permissions
"""
import sys
sys.path.insert(0, '.')

from app.db.database import SessionLocal
from app.db.models import Permission, Role

def ensure_core_permissions():
    db = SessionLocal()
    
    try:
        print("🔐 Checking core permissions...")
        
        # Define core permissions that MUST exist
        core_permissions = [
            {"code": "users.view", "module": "users", "action": "view", "scope": "global", "description": "View users"},
            {"code": "users.create", "module": "users", "action": "create", "scope": "global", "description": "Create users"},
            {"code": "users.edit", "module": "users", "action": "edit", "scope": "global", "description": "Edit users"},
            {"code": "roles.view", "module": "roles", "action": "view", "scope": "global", "description": "View roles"},
        ]
        
        for perm_data in core_permissions:
            existing = db.query(Permission).filter(Permission.code == perm_data["code"]).first()
            if not existing:
                print(f"  ➕ Creating permission: {perm_data['code']}")
                permission = Permission(**perm_data)
                db.add(permission)
            else:
                print(f"  ✅ Exists: {perm_data['code']}")
        
        db.commit()
        
        # Now grant these to Warehouse Admin
        print("\n🔧 Granting to Warehouse Admin...")
        warehouse_admin = db.query(Role).filter(Role.name == 'warehouse_admin').first()
        
        if warehouse_admin:
            current_perms = {p.code for p in warehouse_admin.permissions}
            
            for perm_data in core_permissions:
                if perm_data['code'] not in current_perms:
                    perm = db.query(Permission).filter(Permission.code == perm_data['code']).first()
                    warehouse_admin.permissions.append(perm)
                    print(f"  👍 Granted: {perm_data['code']} to Warehouse Admin")
                else:
                    print(f"  ⏭️  Warehouse Admin already has: {perm_data['code']}")
            
            db.commit()
        else:
            print("❌ Warehouse Admin role not found")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    ensure_core_permissions()
