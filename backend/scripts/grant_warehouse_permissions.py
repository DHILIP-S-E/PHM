"""
Grant Warehouse Admin proper operational permissions
Run with: python -m scripts.grant_warehouse_permissions
"""
import sys
sys.path.insert(0, '.')

from app.db.database import SessionLocal
from app.db.models import Role, Permission

def grant_warehouse_permissions():
    db = SessionLocal()
    
    try:
        print("🔧 Granting Warehouse Admin operational permissions...")
        
        # Get Warehouse Admin role
        warehouse_admin = db.query(Role).filter(Role.name == 'warehouse_admin').first()
        if not warehouse_admin:
            print("  ❌ Warehouse Admin role not found")
            return
        
        # Permission codes that Warehouse Admin should have
        permission_codes = [
            # Dashboard
            'dashboard.view',
            
            # Inventory (warehouse scope)
            'inventory.view.warehouse',
            'inventory.view.global',
            'inventory.entry.warehouse',
            'inventory.adjust.warehouse',
            
            # Dispatches (warehouse scope)
            'dispatches.view.warehouse',
            'dispatches.view.global',
            'dispatches.create.warehouse',
            
            # Purchase Requests (warehouse scope)
            'purchase_requests.view.warehouse',
            'purchase_requests.view.global',
            'purchase_requests.approve.warehouse',
            
            # Employees (warehouse scope)
            'employees.view.warehouse',
            'employees.manage.warehouse',
            
            # Users Management (Warehouse Admin needs these to create staff users)
            'users.view',
            'users.create',
            'users.edit',
            
            # Roles (Hidden for Warehouse Admin)
            # 'roles.view', 
            
            # Attendance (warehouse scope)
            'attendance.manage.warehouse',
            
            # Salary (warehouse scope)
            'salary.manage.warehouse',
            
            # Reports (warehouse scope)
            'reports.view.warehouse',
            'reports.view.global',
            'reports.export',
            
            # Medicines (view only)
            'medicines.view',
            
            # Warehouses (view only)
            'warehouses.view',
            
            # Master Data - VIEW permissions for all modules
            # GST / VAT Slabs
            'gst.view',
            'gst.manage',
            
            # HSN Codes
            'hsn.view',
            'hsn.manage',
            
            # Medicine Categories
            'categories.view',
            'categories.manage',
            
            # Medicine Types
            'medicine_types.view',
            'medicine_types.manage',
            
            # Brands
            'brands.view',
            'brands.manage',
            
            # Manufacturers
            'manufacturers.view',
            'manufacturers.manage',
            
            # Units / Packaging
            'units.view',
            'units.manage',
            
            # Racks
            'racks.view',
            'racks.manage',
            
            # Adjustment Reasons
            'adjustment_reasons.view',
            'adjustment_reasons.manage',
            
            # Suppliers
            'suppliers.view',
            'suppliers.manage',
            
            # Payment Methods
            'payment_methods.view',
            'payment_methods.manage',
        ]
        
        # Get all permissions
        permissions_to_add = db.query(Permission).filter(
            Permission.code.in_(permission_codes)
        ).all()
        
        # Get current permission IDs
        current_perm_ids = set(p.id for p in warehouse_admin.permissions)
        
        # Add new permissions
        added_count = 0
        for perm in permissions_to_add:
            if perm.id not in current_perm_ids:
                warehouse_admin.permissions.append(perm)
                print(f"  ✅ Added: {perm.code}")
                added_count += 1
        
        db.commit()
        
        print(f"\n✅ Permission grant complete!")
        print(f"   Added: {added_count} operational permissions")
        print(f"   Total: {len(warehouse_admin.permissions)} permissions")
        
        print(f"\nWarehouse Admin can now:")
        print(f"  - View and manage warehouse inventory")
        print(f"  - Create and manage dispatches")
        print(f"  - Approve purchase requests")
        print(f"  - Manage warehouse employees")
        print(f"  - View reports")
        print(f"  - Manage master data (from previous script)")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error granting permissions: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    grant_warehouse_permissions()
