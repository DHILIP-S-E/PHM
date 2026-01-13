"""
Add Missing Master Data Permissions
Run with: python -m scripts.add_master_permissions
"""
import sys
sys.path.insert(0, '.')

from app.db.database import SessionLocal
from app.db.models import Permission

def add_master_permissions():
    db = SessionLocal()
    
    try:
        print("🔐 Adding missing master data permissions...")
        
        # Define all missing permissions
        permissions_to_add = [
            # Brands
            {"code": "brands.view", "module": "brands", "action": "view", "scope": "global", "description": "View brands"},
            {"code": "brands.create", "module": "brands", "action": "create", "scope": "global", "description": "Create brands"},
            {"code": "brands.edit", "module": "brands", "action": "edit", "scope": "global", "description": "Edit brands"},
            {"code": "brands.delete", "module": "brands", "action": "delete", "scope": "global", "description": "Delete brands"},
            
            # Manufacturers
            {"code": "manufacturers.view", "module": "manufacturers", "action": "view", "scope": "global", "description": "View manufacturers"},
            {"code": "manufacturers.create", "module": "manufacturers", "action": "create", "scope": "global", "description": "Create manufacturers"},
            {"code": "manufacturers.edit", "module": "manufacturers", "action": "edit", "scope": "global", "description": "Edit manufacturers"},
            {"code": "manufacturers.delete", "module": "manufacturers", "action": "delete", "scope": "global", "description": "Delete manufacturers"},
            
            # Medicine Types
            {"code": "medicine_types.view", "module": "medicine_types", "action": "view", "scope": "global", "description": "View medicine types"},
            {"code": "medicine_types.create", "module": "medicine_types", "action": "create", "scope": "global", "description": "Create medicine types"},
            {"code": "medicine_types.edit", "module": "medicine_types", "action": "edit", "scope": "global", "description": "Edit medicine types"},
            {"code": "medicine_types.delete", "module": "medicine_types", "action": "delete", "scope": "global", "description": "Delete medicine types"},
            
            # Suppliers
            {"code": "suppliers.view", "module": "suppliers", "action": "view", "scope": "global", "description": "View suppliers"},
            {"code": "suppliers.create", "module": "suppliers", "action": "create", "scope": "global", "description": "Create suppliers"},
            {"code": "suppliers.edit", "module": "suppliers", "action": "edit", "scope": "global", "description": "Edit suppliers"},
            {"code": "suppliers.delete", "module": "suppliers", "action": "delete", "scope": "global", "description": "Delete suppliers"},
            
            # Adjustment Reasons
            {"code": "adjustment_reasons.view", "module": "adjustment_reasons", "action": "view", "scope": "global", "description": "View adjustment reasons"},
            {"code": "adjustment_reasons.create", "module": "adjustment_reasons", "action": "create", "scope": "global", "description": "Create adjustment reasons"},
            {"code": "adjustment_reasons.edit", "module": "adjustment_reasons", "action": "edit", "scope": "global", "description": "Edit adjustment reasons"},
            {"code": "adjustment_reasons.delete", "module": "adjustment_reasons", "action": "delete", "scope": "global", "description": "Delete adjustment reasons"},
            
            # Payment Methods
            {"code": "payment_methods.view", "module": "payment_methods", "action": "view", "scope": "global", "description": "View payment methods"},
            {"code": "payment_methods.create", "module": "payment_methods", "action": "create", "scope": "global", "description": "Create payment methods"},
            {"code": "payment_methods.edit", "module": "payment_methods", "action": "edit", "scope": "global", "description": "Edit payment methods"},
            {"code": "payment_methods.delete", "module": "payment_methods", "action": "delete", "scope": "global", "description": "Delete payment methods"},
            
            # Shop Types
            {"code": "shop_types.view", "module": "shop_types", "action": "view", "scope": "global", "description": "View shop types"},
            {"code": "shop_types.create", "module": "shop_types", "action": "create", "scope": "global", "description": "Create shop types"},
            {"code": "shop_types.edit", "module": "shop_types", "action": "edit", "scope": "global", "description": "Edit shop types"},
            {"code": "shop_types.delete", "module": "shop_types", "action": "delete", "scope": "global", "description": "Delete shop types"},
            
            # Customer Types
            {"code": "customer_types.view", "module": "customer_types", "action": "view", "scope": "global", "description": "View customer types"},
            {"code": "customer_types.create", "module": "customer_types", "action": "create", "scope": "global", "description": "Create customer types"},
            {"code": "customer_types.edit", "module": "customer_types", "action": "edit", "scope": "global", "description": "Edit customer types"},
            {"code": "customer_types.delete", "module": "customer_types", "action": "delete", "scope": "global", "description": "Delete customer types"},
            
            # Genders
            {"code": "genders.view", "module": "genders", "action": "view", "scope": "global", "description": "View genders"},
            {"code": "genders.manage", "module": "genders", "action": "manage", "scope": "global", "description": "Manage genders"},
            
            # Employment Types
            {"code": "employment_types.view", "module": "employment_types", "action": "view", "scope": "global", "description": "View employment types"},
            {"code": "employment_types.manage", "module": "employment_types", "action": "manage", "scope": "global", "description": "Manage employment types"},
            
            # Urgency Levels
            {"code": "urgency_levels.view", "module": "urgency_levels", "action": "view", "scope": "global", "description": "View urgency levels"},
            {"code": "urgency_levels.manage", "module": "urgency_levels", "action": "manage", "scope": "global", "description": "Manage urgency levels"},
            
            # Statuses
            {"code": "statuses.view", "module": "statuses", "action": "view", "scope": "global", "description": "View statuses"},
            {"code": "statuses.manage", "module": "statuses", "action": "manage", "scope": "global", "description": "Manage statuses"},
            
            # Designations
            {"code": "designations.view", "module": "designations", "action": "view", "scope": "global", "description": "View designations"},
            {"code": "designations.create", "module": "designations", "action": "create", "scope": "global", "description": "Create designations"},
            {"code": "designations.edit", "module": "designations", "action": "edit", "scope": "global", "description": "Edit designations"},
            {"code": "designations.delete", "module": "designations", "action": "delete", "scope": "global", "description": "Delete designations"},
            
            # Departments
            {"code": "departments.view", "module": "departments", "action": "view", "scope": "global", "description": "View departments"},
            {"code": "departments.create", "module": "departments", "action": "create", "scope": "global", "description": "Create departments"},
            {"code": "departments.edit", "module": "departments", "action": "edit", "scope": "global", "description": "Edit departments"},
            {"code": "departments.delete", "module": "departments", "action": "delete", "scope": "global", "description": "Delete departments"},
        ]
        
        added_count = 0
        skipped_count = 0
        
        for perm_data in permissions_to_add:
            # Check if permission already exists
            existing = db.query(Permission).filter(Permission.code == perm_data["code"]).first()
            
            if existing:
                print(f"  ⏭️  Skipped: {perm_data['code']} (already exists)")
                skipped_count += 1
                continue
            
            # Create new permission
            permission = Permission(**perm_data)
            db.add(permission)
            print(f"  ✅ Added: {perm_data['code']}")
            added_count += 1
        
        db.commit()
        
        print(f"\n✅ Permission migration complete!")
        print(f"   Added: {added_count}")
        print(f"   Skipped: {skipped_count}")
        print(f"   Total: {len(permissions_to_add)}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error adding permissions: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_master_permissions()
