
import sys
import json
from app.db.database import SessionLocal
from app.db.models import (
    MedicineCategory, UnitMaster, HSNMaster, MedicineTypeMaster, BrandMaster, 
    ManufacturerMaster, Role, Warehouse
)

def check_masters():
    db = SessionLocal()
    try:
        print("Checking Master Data in DB...")
        
        counts = {
            "Categories": db.query(MedicineCategory).count(),
            "Units": db.query(UnitMaster).count(),
            "HSN Codes": db.query(HSNMaster).count(),
            "Medicine Types": db.query(MedicineTypeMaster).count(),
            "Brands": db.query(BrandMaster).count(),
            "Manufacturers": db.query(ManufacturerMaster).count(),
            "Roles": db.query(Role).count(),
            "Warehouses": db.query(Warehouse).count(),
        }
        
        print("\nRecord Counts:")
        for k, v in counts.items():
            print(f"  - {k}: {v}")
            
        # specifically check if categories are active
        active_cats = db.query(MedicineCategory).filter(MedicineCategory.is_active == True).count()
        print(f"  - Active Categories: {active_cats}")

        if counts["Categories"] > 0:
            print("\n✅ Database seems populated.")
        else:
            print("\n❌ Database seems EMPTY or connection failed.")

    except Exception as e:
        print(f"❌ Error checking DB: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_masters()
