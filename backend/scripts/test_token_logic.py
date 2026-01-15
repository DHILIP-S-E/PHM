
import sys
import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Constants
BASE_URL = "http://127.0.0.1:8000/api/v1"
LOGIN_URL = f"{BASE_URL}/auth/login"

def decode_jwt(token):
    # Split token into parts
    parts = token.split('.')
    if len(parts) != 3:
        return None
    # Decode payload
    payload_part = parts[1]
    # Add padding if needed
    padding = len(payload_part) % 4
    if padding:
        payload_part += '=' * (4 - padding)
    
    import base64
    return json.loads(base64.urlsafe_b64decode(payload_part).decode('utf-8'))

def test_login_permissions():
    logger.info("🧪 Testing Warehouse Admin Login Permissions...")
    
    # Needs to be a valid warehouse admin credentials
    # Assuming standard dev credentials, but I might need to look them up if this fails
    # Based on previous contexts, we often had admin@example.com, but I need warehouse admin
    
    # I'll first list users to find a warehouse admin
    sys.path.insert(0, '.')
    from app.db.database import SessionLocal
    from app.db.models import Role, User
    
    db = SessionLocal()
    try:
        wa_role = db.query(Role).filter(Role.name == 'warehouse_admin').first()
        if not wa_role:
            logger.error("❌ Warehouse Admin role not found")
            return
            
        wa_user = db.query(User).filter(User.role_id == wa_role.id).first()
        if not wa_user:
            logger.error("❌ No Warehouse Admin user found")
            return
            
        email = wa_user.email
        logger.info(f"Found WA User: {email}")
        
        # NOTE: I don't have the password. 
        # But I can use the same logic as `auth.py` to generate what the token SHOULD be
        # to verify the permissions logic, without actually logging in via HTTP if I don't know the password.
        # OR I can reset the password to something known in this script (safe for dev)
        
        # Let's verify the permission logic directly first (simulating login)
        from app.api.v1.auth import get_user_permissions
        
        perms = get_user_permissions(db, wa_user)
        logger.info(f"Simulated Permissions for {email}:")
        
        target_perms = ["gst.view", "hsn.view", "categories.view", "racks.view"]
        
        all_good = True
        for p in target_perms:
            if p in perms:
                logger.info(f"  ✅ {p} found")
            else:
                logger.info(f"  ❌ {p} NOT found")
                all_good = False
                
        if all_good:
            logger.info("\n✅ Backend logic is identifying permissions correctly.")
            logger.info("👉 If the frontend still gets 403, the user MUST log out and log back in to get a new token.")
        else:
            logger.error("\n❌ Backend logic failed to find permissions. Debug `get_user_permissions`.")

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_login_permissions()
