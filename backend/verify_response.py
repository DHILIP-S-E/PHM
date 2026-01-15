
import sys
from app.db.database import SessionLocal
from app.api.v1.unified_masters import AllMastersResponse, CategoryResponse, UnitResponse
from app.db.models import (
    MedicineCategory, UnitMaster, HSNMaster, Rack, Role, Warehouse, MedicalShop,
    PaymentMethodMaster, ShopTypeMaster, CustomerTypeMaster, MedicineTypeMaster,
    GSTSlabMaster, GenderMaster, EmploymentTypeMaster, UrgencyMaster,
    StatusMaster, DesignationMaster, DepartmentMaster, BrandMaster, ManufacturerMaster,
    SupplierMaster, AdjustmentReasonMaster
)

def verify_response():
    db = SessionLocal()
    try:
        print("Constructing AllMastersResponse...")
        
        # Helper to mimic filter_active logic
        def get_all(model):
            return db.query(model).all() # Ignoring active filter for robustness check
            
        # Manually constructing the dictionary first to catch which key fails
        data = {
            "categories": get_all(MedicineCategory),
            "units": get_all(UnitMaster),
            "hsn_codes": get_all(HSNMaster),
            "medicine_types": get_all(MedicineTypeMaster),
            "payment_methods": get_all(PaymentMethodMaster),
            "shop_types": get_all(ShopTypeMaster),
            "customer_types": get_all(CustomerTypeMaster),
            "gst_slabs": get_all(GSTSlabMaster),
            "genders": get_all(GenderMaster),
            "employment_types": get_all(EmploymentTypeMaster),
            "urgency_levels": get_all(UrgencyMaster),
            "statuses": get_all(StatusMaster),
            "designations": get_all(DesignationMaster),
            "departments": get_all(DepartmentMaster),
            "roles": db.query(Role).filter(Role.is_creatable == True).all(),
            "warehouses": get_all(Warehouse),
            "shops": get_all(MedicalShop),
            "racks": get_all(Rack),
            "brands": get_all(BrandMaster),
            "manufacturers": get_all(ManufacturerMaster),
            "suppliers": get_all(SupplierMaster),
            "adjustment_reasons": get_all(AdjustmentReasonMaster),
        }
        
        print("Data queries done. Validating Pydantic model...")
        
        try:
            resp = AllMastersResponse(**data)
            print("✅ Pydantic validation SUCCESS!")
        except Exception as e:
            print(f"❌ Pydantic validation FAILED: {e}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"❌ Error querying DB: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_response()
