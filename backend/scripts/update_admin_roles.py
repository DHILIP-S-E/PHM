"""
Update Warehouse Admin and Pharmacy Admin roles with master data permissions
Give them Create, Read, Update but NOT Delete permissions
Run with: python -m scripts.update_admin_roles
"""
import sys
sys.path.insert(0, '.')

from app.db.database import SessionLocal
from app.db.models import Role, Permission

def update_admin_roles():
    db = SessionLocal()
    
    try:
        print("🔧 Updating Warehouse Admin and Pharmacy Admin roles...")
        
        # Master data modules that admins should have CRU (not D) access to
        master_data_modules = [
            'brands',
            'manufacturers',
            'medicine_types',
            'suppliers',
            'adjustment_reasons',
            'payment_methods',
            'shop_types',
            'customer_types',
            'genders',
            'employment_types',
            'urgency_levels',
            'statuses',
            'designations',
            'departments',
            'categories',
            'units',
            'hsn',
            'racks',
            'gst',
        ]
        
        # Actions to grant (excluding 'delete')
        allowed_actions = ['view', 'create', 'edit', 'manage']
        
        # Get all permissions for these modules (excluding delete)
        permissions_to_add = []
        for module in master_data_modules:
            perms = db.query(Permission).filter(
                Permission.module == module,
                Permission.action.in_(allowed_actions)
            ).all()
            permissions_to_add.extend(perms)
        
        print(f"  Found {len(permissions_to_add)} master data permissions (CRU only)")
        
        # Update Warehouse Admin role
        warehouse_admin = db.query(Role).filter(Role.name == 'warehouse_admin').first()
        if warehouse_admin:
            # Get current permission IDs
            current_perm_ids = set(p.id for p in warehouse_admin.permissions)
            new_perm_ids = set(p.id for p in permissions_to_add)
            
            # Add new permissions
            for perm in permissions_to_add:
                if perm.id not in current_perm_ids:
                    warehouse_admin.permissions.append(perm)
            
            print(f"  ✅ Updated Warehouse Admin role")
            print(f"     Added {len(new_perm_ids - current_perm_ids)} new permissions")
        else:
            print("  ⚠️  Warehouse Admin role not found")
        
        # Update Pharmacy Admin role (if exists)
        pharmacy_admin = db.query(Role).filter(Role.name == 'pharmacy_admin').first()
        if pharmacy_admin:
            # Get current permission IDs
            current_perm_ids = set(p.id for p in pharmacy_admin.permissions)
            new_perm_ids = set(p.id for p in permissions_to_add)
            
            # Add new permissions
            for perm in permissions_to_add:
                if perm.id not in current_perm_ids:
                    pharmacy_admin.permissions.append(perm)
            
            print(f"  ✅ Updated Pharmacy Admin role")
            print(f"     Added {len(new_perm_ids - current_perm_ids)} new permissions")
        else:
            print("  ℹ️  Pharmacy Admin role not found (will skip)")
        
        db.commit()
        
        print(f"\n✅ Role update complete!")
        print(f"\nPermissions granted:")
        print(f"  - View master data")
        print(f"  - Create master data")
        print(f"  - Edit/Update master data")
        print(f"  - Manage master data")
        print(f"\nPermissions NOT granted:")
        print(f"  - Delete master data (Super Admin only)")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error updating roles: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    update_admin_roles()
