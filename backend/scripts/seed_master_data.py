
"""
Master Data Seed Script
Populates: Medicine Categories, HSN Codes, Medicine Types, Units, Racks, and Expanded Medicine Catalog
Run with: python -m scripts.seed_master_data
"""
import sys
import random
from datetime import date, timedelta, datetime

sys.path.insert(0, '.')

from app.db.database import SessionLocal
from app.db.models import (
    Medicine, MedicineCategory, HSNMaster, UnitMaster, Rack,
    Warehouse, MedicalShop, MedicineType, Batch, WarehouseStock
)

def seed_master_data():
    db = SessionLocal()
    try:
        print("🌱 Starting Master Data Seed...")

        # 1. Medicine Categories
        print("  1. Seeding Medicine Categories...")
        categories = [
            ("Antibiotics", "Medications that fight bacterial infections"),
            ("Analgesics", "Pain relievers"),
            ("Antipyretics", "Fever reducers"),
            ("Antiseptics", "Substances that stop or slow the growth of microorganisms"),
            ("Vitamins & Supplements", "Dietary supplements"),
            ("Cardiovascular", "Heart and blood vessel medication"),
            ("Gastrointestinal", "Digestive system medication"),
            ("Respiratory", "Breathing and lung medication"),
            ("Dermatological", "Skin medication"),
        ]
        
        cat_map = {}
        for name, desc in categories:
            cat = db.query(MedicineCategory).filter(MedicineCategory.name == name).first()
            if not cat:
                cat = MedicineCategory(name=name, description=desc)
                db.add(cat)
                print(f"     + Created Category: {name}")
            cat_map[name] = cat
        db.flush()

        # 2. HSN Codes
        print("  2. Seeding HSN Codes...")
        hsn_codes = [
            ("300490", "Medicaments for therapeutic or prophylactic uses", 12.0),
            ("300450", "Vitamins and their derivatives", 18.0),
            ("300310", "Medicaments containing penicillin", 12.0),
            ("300420", "Medicaments containing other antibiotics", 12.0),
            ("300430", "Medicaments containing hormones", 12.0),
            ("9018", "Medical instruments and appliances", 18.0),
        ]
        
        for code, desc, rate in hsn_codes:
            hsn = db.query(HSNMaster).filter(HSNMaster.hsn_code == code).first()
            if not hsn:
                hsn = HSNMaster(
                    hsn_code=code, 
                    description=desc, 
                    gst_rate=rate,
                    cgst_rate=rate/2,
                    sgst_rate=rate/2
                )
                db.add(hsn)
                print(f"     + Created HSN: {code}")
        db.flush()

        # 3. Unit Master
        print("  3. Seeding Unit Master...")
        units = [
            ("Strip", "strip", "Standard strip of tablets/capsules"),
            ("Bottle", "btl", "Liquid bottle"),
            ("Box", "box", "Cardboard box"),
            ("Vial", "vial", "Injection vial"),
            ("Tube", "tube", "Ointment tube"),
            ("Sachet", "sachet", "Powder sachet"),
            ("Jar", "jar", "Plastic/Glass jar"),
        ]

        for name, short, desc in units:
            unit = db.query(UnitMaster).filter(UnitMaster.name == name).first()
            if not unit:
                unit = UnitMaster(name=name, short_name=short, description=desc)
                db.add(unit)
                print(f"     + Created Unit: {name}")
        db.flush()

        # 4. Racks (for existing Warehouses and Shops)
        print("  4. Seeding Racks...")
        warehouses = db.query(Warehouse).all()
        shops = db.query(MedicalShop).all()
        
        # Warehouse Racks
        for wh in warehouses:
            for section in ['A', 'B', 'C']:
                for row in range(1, 4):
                    rack_no = f"WH-{wh.code[-3:]}-{section}-{row}"
                    rack = db.query(Rack).filter(Rack.rack_number == rack_no).first()
                    if not rack:
                        rack = Rack(
                            rack_name=f"Section {section} Row {row}",
                            rack_number=rack_no,
                            warehouse_id=wh.id,
                            section=section,
                            floor="Ground"
                        )
                        db.add(rack)
        
        # Shop Racks
        for sh in shops:
            for section in ['F', 'R']: # Front, Rear
                for row in range(1, 3):
                    rack_no = f"SH-{sh.code[-3:]}-{section}-{row}"
                    rack = db.query(Rack).filter(Rack.rack_number == rack_no).first()
                    if not rack:
                        rack = Rack(
                            rack_name=f"{'Front' if section=='F' else 'Rear'} Row {row}",
                            rack_number=rack_no,
                            shop_id=sh.id,
                            section=section
                        )
                        db.add(rack)
        db.flush()

        # 5. Expanded Medicines Catalog
        print("  5. Seeding Expanded Medicine Catalog...")
        # (Name, Generic, Manufacturer, Type, CategoryName, MRP, PurchasePrice)
        new_medicines = [
            ("Augmentin 625 Duo", "Amoxicillin + Clavulanic Acid", "GSK", MedicineType.TABLET, "Antibiotics", 220.0, 150.0),
            ("Dolo 650", "Paracetamol", "Micro Labs", MedicineType.TABLET, "Antipyretics", 32.0, 18.0),
            ("Pan 40", "Pantoprazole", "Alkem", MedicineType.TABLET, "Gastrointestinal", 155.0, 90.0),
            ("Becosules", "B-Complex + Vit C", "Pfizer", MedicineType.CAPSULE, "Vitamins & Supplements", 45.0, 30.0),
            ("Ascoril LS", "Levosalbutamol + Ambroxol", "Glenmark", MedicineType.SYRUP, "Respiratory", 115.0, 75.0),
            ("Volini Gel", "Diclofenac", "Sun Pharma", MedicineType.OINTMENT, "Analgesics", 140.0, 95.0),
            ("Betadine Sol", "Povidone Iodine", "Win-Medicare", MedicineType.DROPS, "Antiseptics", 85.0, 55.0),
            ("Telma 40", "Telmisartan", "Glenmark", MedicineType.TABLET, "Cardiovascular", 240.0, 160.0),
            ("Shelcal 500", "Calcium + Vit D3", "Torrent", MedicineType.TABLET, "Vitamins & Supplements", 120.0, 80.0),
            ("Allegra 120", "Fexofenadine", "Sanofi", MedicineType.TABLET, "Respiratory", 190.0, 130.0),
            ("Crocin Advance", "Paracetamol", "GSK", MedicineType.TABLET, "Antipyretics", 20.0, 12.0),
            ("Glycomet 500", "Metformin", "USV", MedicineType.TABLET, "Cardiovascular", 55.0, 35.0),
            ("Rantac 150", "Ranitidine", "JB Chemicals", MedicineType.TABLET, "Gastrointestinal", 30.0, 18.0),
            ("Neurobion Forte", "Vit B1+B6+B12", "Merck", MedicineType.TABLET, "Vitamins & Supplements", 40.0, 25.0),
            ("Otrivin Oxy", "Oxymetazoline", "GSK", MedicineType.DROPS, "Respiratory", 60.0, 40.0),
        ]

        added_meds = []
        for name, generic, mfr, mtype, cat_name, mrp, pp in new_medicines:
            med = db.query(Medicine).filter(Medicine.name == name).first()
            if not med:
                med = Medicine(
                    name=name,
                    generic_name=generic,
                    manufacturer=mfr,
                    medicine_type=mtype,
                    category=cat_name,  # Storing name directly as per model, or could link to ID if schema updated
                    mrp=mrp,
                    purchase_price=pp,
                    gst_rate=12.0 if cat_name != "Vitamins & Supplements" else 18.0,
                    pack_size=10,
                    reorder_level=100,
                    is_active=True
                )
                db.add(med)
                added_meds.append(med)
                print(f"     + Created Medicine: {name}")
            else:
                added_meds.append(med)
        
        db.flush()

        # 6. Create Initial Stock (Batches) for New Medicines
        if added_meds and warehouses:
            print("  6. Creating Batches & Stock for new medicines...")
            wh = warehouses[0] # Stock primarily in main warehouse
            
            for med in added_meds:
                # Check if batches already exist
                existing_batch = db.query(Batch).filter(Batch.medicine_id == med.id).first()
                if existing_batch:
                    continue

                # Create 2 batches
                for i in range(2):
                    batch = Batch(
                        medicine_id=med.id,
                        batch_number=f"B-{med.name[:3].upper()}-{random.randint(100,999)}",
                        manufacturing_date=date.today() - timedelta(days=random.randint(30, 180)),
                        expiry_date=date.today() + timedelta(days=random.randint(180, 720)),
                        quantity=random.randint(500, 2000),
                        purchase_price=med.purchase_price,
                        mrp=med.mrp,
                        supplier="PharmaDistro Ltd"
                    )
                    db.add(batch)
                    db.flush()

                    # Add to Warehouse Stock
                    wh_stock = WarehouseStock(
                        warehouse_id=wh.id,
                        medicine_id=med.id,
                        batch_id=batch.id,
                        quantity=batch.quantity,
                        rack_number=f"WH-{wh.code[-3:]}-A-1" # Simplified assignment
                    )
                    db.add(wh_stock)
        
        db.commit()
        print("✅ Master Data Seeded Successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding master data: {e}")
        # raise # Optional: don't crash if one thing fails, but good to know
    finally:
        db.close()

if __name__ == "__main__":
    seed_master_data()
