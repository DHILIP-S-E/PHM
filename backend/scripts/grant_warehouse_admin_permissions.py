"""
Grant comprehensive permissions to Warehouse Admin role
Based on 9 core modules for warehouse operations management
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

def grant_warehouse_admin_permissions():
    db: Session = SessionLocal()
    
    try:
        # Find Warehouse Admin role
        warehouse_admin = db.query(Role).filter(Role.name == "warehouse_admin").first()
        if not warehouse_admin:
            print("❌ Warehouse Admin role not found!")
            return
        
        print(f"✅ Found Warehouse Admin role: {warehouse_admin.id}")
        
        # Define all permissions for Warehouse Admin based on 9 modules
        warehouse_admin_permissions = [
            # ═══════════════════════════════════════════════════════════════
            # 🔐 USER MANAGEMENT (WAREHOUSE-SCOPED ONLY)
            # Can create/manage users ONLY for their warehouse
            # Can assign only: warehouse_employee, warehouse_supervisor, inventory_manager
            # Cannot assign: warehouse_admin, super_admin
            # ═══════════════════════════════════════════════════════════════
            "users.view.warehouse",           # View users in their warehouse
            "users.create.warehouse",         # Create users for their warehouse
            "users.update.warehouse",         # Update users in their warehouse
            "users.delete.warehouse",         # Deactivate users in their warehouse
            
            # ═══════════════════════════════════════════════════════════════
            # 1️⃣ WAREHOUSE MANAGEMENT
            # ═══════════════════════════════════════════════════════════════
            "warehouses.view.warehouse",      # View own warehouse profile
            "warehouses.update.warehouse",    # Update warehouse profile
            "warehouse_staff.view",           # View warehouse staff
            "warehouse_staff.manage",         # Manage warehouse staff
            "shops.view.warehouse",           # View assigned shops
            
            # ═══════════════════════════════════════════════════════════════
            # 2️⃣ INVENTORY MANAGEMENT
            # ═══════════════════════════════════════════════════════════════
            "inventory.view.warehouse",       # View warehouse inventory
            "inventory.manage.warehouse",     # Manage warehouse inventory
            "stock.entry.warehouse",          # Add stock to warehouse
            "stock.adjust.warehouse",         # Adjust stock levels
            "stock.transfer.warehouse",       # Transfer stock between warehouses
            "batches.view.warehouse",         # View batches
            "batches.manage.warehouse",       # Manage batches
            "expiry.view.warehouse",          # View expiry tracking
            "expiry.manage.warehouse",        # Manage expiry alerts
            "stock_alerts.view.warehouse",    # View stock alerts
            "stock_alerts.manage.warehouse",  # Manage stock thresholds
            
            # ═══════════════════════════════════════════════════════════════
            # 3️⃣ PURCHASE & DISPATCH
            # ═══════════════════════════════════════════════════════════════
            "purchase_requests.view.warehouse",   # View shop purchase requests
            "purchase_requests.approve",          # Approve purchase requests
            "purchase_requests.reject",           # Reject purchase requests
            "dispatches.view.warehouse",          # View dispatches
            "dispatches.create.warehouse",        # Create dispatch orders
            "dispatches.update.warehouse",        # Update dispatch status
            "dispatches.manage.warehouse",        # Full dispatch management
            
            # ═══════════════════════════════════════════════════════════════
            # 4️⃣ MEDICINE CATALOG (LIMITED)
            # ═══════════════════════════════════════════════════════════════
            "medicines.view.warehouse",       # View medicines
            "medicines.create.warehouse",     # Add local medicines
            "medicines.update.warehouse",     # Update medicine details
            "medicine_pricing.manage.warehouse", # Manage pricing
            
            # ═══════════════════════════════════════════════════════════════
            # 5️⃣ SHOP OVERSIGHT
            # ═══════════════════════════════════════════════════════════════
            "shops.view.warehouse",           # View assigned shops
            "shop_performance.view",          # View shop performance
            "shop_inventory.view",            # View shop inventory status
            "shop_analytics.view",            # View shop analytics
            
            # ═══════════════════════════════════════════════════════════════
            # 6️⃣ TAX & ACCOUNTING
            # ═══════════════════════════════════════════════════════════════
            "gst_reports.view.warehouse",     # View GST reports
            "tax_reports.view.warehouse",     # View tax reports
            "purchase_tax.view.warehouse",    # View purchase tax
            "returns.view.warehouse",         # View returns
            "returns.manage.warehouse",       # Manage returns
            
            # ═══════════════════════════════════════════════════════════════
            # 7️⃣ REPORTS & ANALYTICS
            # ═══════════════════════════════════════════════════════════════
            "reports.view.warehouse",         # View warehouse reports
            "analytics.view.warehouse",       # View analytics
            "sales_reports.view.warehouse",   # View sales summary
            "dispatch_reports.view.warehouse", # View dispatch performance
            "inventory_reports.view.warehouse", # View inventory aging
            "performance_reports.view.warehouse", # View performance reports
            
            # ═══════════════════════════════════════════════════════════════
            # 8️⃣ HR MANAGEMENT
            # ═══════════════════════════════════════════════════════════════
            "employees.view.warehouse",       # View warehouse employees
            "employees.create.warehouse",     # Add warehouse employees (NOT users with roles)
            "employees.update.warehouse",     # Update employee details
            "attendance.view.warehouse",      # View attendance
            "attendance.manage.warehouse",    # Manage attendance
            "payroll.view.warehouse",         # View payroll
            "payroll.process.warehouse",      # Process payroll
            "leave.view.warehouse",           # View leave requests
            "leave.manage.warehouse",         # Manage leave requests
            
            # ═══════════════════════════════════════════════════════════════
            # 9️⃣ NOTIFICATIONS & ALERTS
            # ═══════════════════════════════════════════════════════════════
            "notifications.view.warehouse",   # View notifications
            "alerts.view.warehouse",          # View alerts
            "low_stock_alerts.view",          # View low stock alerts
            "expiry_alerts.view",             # View expiry alerts
            "dispatch_alerts.view",           # View dispatch alerts
            
            # ═══════════════════════════════════════════════════════════════
            # MASTER DATA (CREATE, UPDATE - NO DELETE)
            # Warehouse Admin can add/edit master data but cannot delete
            # ═══════════════════════════════════════════════════════════════
            "categories.view",                # View medicine categories
            "categories.create",              # Create new categories
            "categories.update",              # Update categories
            
            "units.view",                     # View units
            "units.create",                   # Create new units
            "units.update",                   # Update units
            
            "brands.view",                    # View brands
            "brands.create",                  # Create new brands
            "brands.update",                  # Update brands
            
            "manufacturers.view",             # View manufacturers
            "manufacturers.create",           # Create new manufacturers
            "manufacturers.update",           # Update manufacturers
            
            "medicine_types.view",            # View medicine types
            "medicine_types.create",          # Create new medicine types
            "medicine_types.update",          # Update medicine types
            
            "hsn.view",                       # View HSN codes
            "hsn.create",                     # Create new HSN codes
            "hsn.update",                     # Update HSN codes
            
            "gst.view",                       # View GST slabs
            "gst.create",                     # Create new GST slabs
            "gst.update",                     # Update GST slabs
            
            "suppliers.view",                 # View suppliers
            "suppliers.create",               # Create new suppliers
            "suppliers.update",               # Update suppliers
            
            "payment_methods.view",           # View payment methods
            "payment_methods.create",         # Create new payment methods
            "payment_methods.update",         # Update payment methods
            
            "adjustment_reasons.view",        # View adjustment reasons
            "adjustment_reasons.create",      # Create new adjustment reasons
            "adjustment_reasons.update",      # Update adjustment reasons
            
            "racks.view",                     # View racks
            "racks.create",                   # Create new racks
            "racks.update",                   # Update racks
            "racks.manage.warehouse",         # Manage warehouse racks
        ]
        
        print(f"\n📋 Granting {len(warehouse_admin_permissions)} permissions to Warehouse Admin...")
        
        granted_count = 0
        missing_permissions = []
        
        for perm_code in warehouse_admin_permissions:
            # Find the permission
            permission = db.query(Permission).filter(Permission.code == perm_code).first()
            
            if not permission:
                missing_permissions.append(perm_code)
                print(f"⚠️  Permission not found: {perm_code}")
                continue
            
            # Check if already assigned
            existing = db.query(RolePermission).filter(
                RolePermission.role_id == warehouse_admin.id,
                RolePermission.permission_id == permission.id
            ).first()
            
            if not existing:
                role_perm = RolePermission(
                    role_id=warehouse_admin.id,
                    permission_id=permission.id
                )
                db.add(role_perm)
                granted_count += 1
                print(f"✅ Granted: {perm_code}")
            else:
                print(f"⏭️  Already exists: {perm_code}")
        
        db.commit()
        
        print(f"\n{'='*60}")
        print(f"✅ Successfully granted {granted_count} new permissions")
        print(f"⏭️  {len(warehouse_admin_permissions) - granted_count - len(missing_permissions)} already existed")
        
        if missing_permissions:
            print(f"\n⚠️  {len(missing_permissions)} permissions not found in database:")
            for perm in missing_permissions:
                print(f"   - {perm}")
            print("\n💡 These permissions need to be created first!")
        
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Granting Warehouse Admin Permissions...")
    print("="*60)
    grant_warehouse_admin_permissions()
