"""
Seed employment types and genders master data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import MasterOption

def seed_employment_and_gender():
    db = SessionLocal()
    try:
        print("\n=== Seeding Employment Types and Genders ===\n")
        
        # Employment Types
        employment_types = [
            {"code": "full_time", "label": "Full Time", "category": "employment_types"},
            {"code": "part_time", "label": "Part Time", "category": "employment_types"},
            {"code": "contract", "label": "Contract", "category": "employment_types"},
            {"code": "intern", "label": "Intern", "category": "employment_types"},
        ]
        
        # Genders
        genders = [
            {"code": "male", "label": "Male", "category": "genders"},
            {"code": "female", "label": "Female", "category": "genders"},
            {"code": "other", "label": "Other", "category": "genders"},
        ]
        
        all_data = employment_types + genders
        
        for item in all_data:
            # Check if already exists
            existing = db.query(MasterOption).filter(
                MasterOption.category == item["category"],
                MasterOption.code == item["code"]
            ).first()
            
            if not existing:
                master = MasterOption(
                    category=item["category"],
                    code=item["code"],
                    name=item["name"],
                    is_active=True
                )
                db.add(master)
                print(f"✅ Added: {item['category']} - {item['name']}")
            else:
                print(f"⏭️  Skipped (exists): {item['category']} - {item['name']}")
        
        db.commit()
        print("\n✅ Seeding completed successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_employment_and_gender()
