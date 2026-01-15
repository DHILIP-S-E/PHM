"""
Check specific user's role and permissions
Run with: python -m scripts.check_user_permissions war@gmail.com
"""
import sys
sys.path.insert(0, '.')

from app.db.database import SessionLocal
from app.db.models import User, Role

def check_user(email):
    db = SessionLocal()
    
    try:
        print(f"🔍 Checking user: {email}\n")
        
        # Get user
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"  ❌ User not found: {email}")
            return
        
        print(f"✅ User found:")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Full Name: {user.full_name}")
        print(f"   Role (enum): {user.role}")
        print(f"   Role ID (FK): {user.role_id}")
        print(f"   Warehouse ID: {user.assigned_warehouse_id}")
        print(f"   Shop ID: {user.assigned_shop_id}")
        print()
        
        # Check role_id
        if user.role_id:
            role = db.query(Role).filter(Role.id == user.role_id).first()
            if role:
                print(f"✅ Role (via role_id FK):")
                print(f"   Name: {role.name}")
                print(f"   Permissions: {len(role.permissions)}")
                print()
                print("   Permission codes:")
                for perm in sorted(role.permissions, key=lambda p: p.code):
                    print(f"     • {perm.code}")
            else:
                print(f"❌ Role not found for role_id: {user.role_id}")
        else:
            print("⚠️  No role_id set, checking role enum...")
            role_name = user.role.value if hasattr(user.role, 'value') else str(user.role)
            print(f"   Role enum value: {role_name}")
            
            role = db.query(Role).filter(Role.name == role_name).first()
            if role:
                print(f"✅ Role found (via enum):")
                print(f"   Name: {role.name}")
                print(f"   Permissions: {len(role.permissions)}")
            else:
                print(f"❌ Role not found for name: {role_name}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    email = sys.argv[1] if len(sys.argv) > 1 else "war@gmail.com"
    check_user(email)
