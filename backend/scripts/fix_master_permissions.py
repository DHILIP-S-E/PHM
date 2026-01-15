"""
Fix and grant master data permissions for Warehouse Admin
This script ensures all master data permissions exist in the database and assigns
Create/Read/Update (CRU) access to the Warehouse Admin role.
"""
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, '.')

from app.db.database import SessionLocal
from app.db.models import Role, Permission

def fix_master_permissions():
    db = SessionLocal()
    
    try:
        logger.info("🔧 Starting Master Data Permission Fix...")
        
        # 1. Define all master modules and their permission scopes
        # Format: (code_prefix, human_readable_name)
        master_modules = [
            ("gst", "GST / VAT Slabs"),
            ("hsn", "HSN Codes"),
            ("categories", "Medicine Categories"),
            ("medicine_types", "Medicine Types"),
            ("brands", "Brands"),
            ("manufacturers", "Manufacturers"),
            ("units", "Units / Packaging"),
            ("racks", "Rack Master"),
            ("adjustment_reasons", "Adjustment Reasons"),
            ("suppliers", "Suppliers"),
            ("payment_methods", "Payment Methods"),
            
            # Extras (good to have just in case)
            ("shop_types", "Shop Types"),
            ("customer_types", "Customer Types"),
            ("genders", "Genders"),
            ("employment_types", "Employment Types"),
            ("urgency_levels", "Urgency Levels"),
            ("statuses", "Statuses"),
            ("designations", "Designations"),
            ("departments", "Departments"),
        ]
        
        # 2. Ensure permissions exist in the database
        logger.info("\n🔐 Ensuring permissions exist in database...")
        actions = [
            ("view", "View"),
            ("create", "Create"),
            ("edit", "Edit"),
            ("delete", "Delete")
        ]
        
        for prefix, module_name in master_modules:
            for action_code, action_name in actions:
                perm_code = f"{prefix}.{action_code}"
                existing = db.query(Permission).filter(Permission.code == perm_code).first()
                
                if not existing:
                    logger.info(f"  ➕ Creating permission: {perm_code}")
                    perm = Permission(
                        code=perm_code,
                        module=prefix,
                        action=action_code,
                        scope="global",  # Master data is usually global
                        description=f"{action_name} {module_name}"
                    )
                    db.add(perm)
                # else:
                #     logger.info(f"  ✅ Exists: {perm_code}")
        
        db.commit()
        
        # 3. Grant CRU (Create, Read, Update) to Warehouse Admin
        logger.info("\n👤 Granting CRU permissions to Warehouse Admin...")
        
        warehouse_admin = db.query(Role).filter(Role.name == 'warehouse_admin').first()
        if not warehouse_admin:
            logger.error("❌ Warehouse Admin role not found!")
            return
        
        current_perm_ids = {p.id for p in warehouse_admin.permissions}
        
        # We want to grant view, create, edit. We explicitly exclude delete.
        actions_to_grant = ["view", "create", "edit"]
        
        # Target only the requested modules + likely useful ones
        target_prefixes = [
            "gst", "hsn", "categories", "medicine_types", "brands", 
            "manufacturers", "units", "racks", "adjustment_reasons", 
            "suppliers", "payment_methods"
        ]
        
        granted_count = 0
        
        for prefix in target_prefixes:
            for action in actions_to_grant:
                perm_code = f"{prefix}.{action}"
                perm = db.query(Permission).filter(Permission.code == perm_code).first()
                
                if perm and perm.id not in current_perm_ids:
                    warehouse_admin.permissions.append(perm)
                    current_perm_ids.add(perm.id)
                    logger.info(f"  ✅ Granted: {perm_code}")
                    granted_count += 1
                elif not perm:
                    logger.warning(f"  ⚠️  Permission not found (unexpected): {perm_code}")
        
        db.commit()
        
        logger.info(f"\n🎉 Done! Granted {granted_count} new permissions.")
        logger.info("Warehouse Admin now has Create/Edit/View access to all requested master data.")

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    fix_master_permissions()
