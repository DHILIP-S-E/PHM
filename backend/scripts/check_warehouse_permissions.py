"""
Diagnostic script to check Warehouse Admin permissions
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
from app.db.models import Role, Permission, RolePermission

def check_warehouse_admin_permissions():
    db: Session = SessionLocal()
    
    try:
        # Find Warehouse Admin role
        warehouse_admin = db.query(Role).filter(Role.name == "warehouse_admin").first()
        if not warehouse_admin:
            print("ERROR: Warehouse Admin role not found!")
            return
        
        print(f"Found Warehouse Admin role: {warehouse_admin.id}")
        print(f"Role name: {warehouse_admin.name}")
        print(f"Description: {warehouse_admin.description}")
        print(f"Entity type: {warehouse_admin.entity_type}")
        print(f"Is creatable: {warehouse_admin.is_creatable}")
        print(f"Is system: {warehouse_admin.is_system}")
        print("\n" + "="*60)
        
        # Get all permissions for this role
        role_permissions = db.query(RolePermission).filter(
            RolePermission.role_id == warehouse_admin.id
        ).all()
        
        print(f"\nTotal permissions assigned: {len(role_permissions)}")
        print("="*60)
        
        # Get permission details
        permission_codes = []
        for rp in role_permissions:
            perm = db.query(Permission).filter(Permission.id == rp.permission_id).first()
            if perm:
                permission_codes.append(perm.code)
        
        # Group by module
        modules = {}
        for code in sorted(permission_codes):
            module = code.split('.')[0]
            if module not in modules:
                modules[module] = []
            modules[module].append(code)
        
        print("\nPermissions by module:")
        print("="*60)
        for module, perms in sorted(modules.items()):
            print(f"\n{module.upper()} ({len(perms)} permissions):")
            for perm in perms:
                print(f"  - {perm}")
        
        # Check for user management permissions specifically
        print("\n" + "="*60)
        print("USER MANAGEMENT PERMISSIONS:")
        print("="*60)
        user_perms = [p for p in permission_codes if p.startswith('users.')]
        if user_perms:
            for perm in user_perms:
                print(f"  ✓ {perm}")
        else:
            print("  ✗ NO USER MANAGEMENT PERMISSIONS FOUND!")
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("Checking Warehouse Admin Permissions...")
    print("="*60)
    check_warehouse_admin_permissions()
