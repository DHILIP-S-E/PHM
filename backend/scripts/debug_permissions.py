
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, '.')

from app.db.database import SessionLocal
from app.db.models import Role, Permission, User

def debug_permissions():
    db = SessionLocal()
    
    try:
        logger.info("🔍 Debugging Warehouse Admin Permissions...")
        
        # 1. Get Role
        role = db.query(Role).filter(Role.name == 'warehouse_admin').first()
        if not role:
            logger.error("❌ Role 'warehouse_admin' not found!")
            return

        logger.info(f"Role: {role.name} (ID: {role.id})")
        
        # 2. List Permissions
        permissions = sorted([p.code for p in role.permissions])
        logger.info(f"Total Permissions: {len(permissions)}")
        
        # Check specifically for the ones failing
        critical_perms = [
            "gst.view", 
            "hsn.view", 
            "categories.view", 
            "units.view"
        ]
        
        logger.info("\nChecking Critical Permissions:")
        for code in critical_perms:
            has_perm = code in permissions
            icon = "✅" if has_perm else "❌"
            logger.info(f"  {icon} {code}")

        # 3. Check User Role (optional, listing first few users with this role)
        users = db.query(User).filter(User.role_id == role.id).all()
        logger.info(f"\nUsers with this role ({len(users)}):")
        for u in users:
            logger.info(f"  - {u.full_name} ({u.email})")

    except Exception as e:
        logger.error(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_permissions()
