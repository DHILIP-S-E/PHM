"""
Script to add missing SSOT master tables and data
"""
import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text, inspect
from app.core.config import settings

def generate_uuid():
    return str(uuid.uuid4())

def main():
    print(f"Connecting to database...")
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        # Check if shop_type_master table exists
        if 'shop_type_master' not in tables:
            print("Creating shop_type_master table...")
            conn.execute(text("""
                CREATE TABLE shop_type_master (
                    id VARCHAR(36) PRIMARY KEY,
                    code VARCHAR(20) UNIQUE NOT NULL,
                    name VARCHAR(50) NOT NULL,
                    description TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    sort_order INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_shop_type_code ON shop_type_master(code)"))
            
            # Seed shop types
            shop_types = [
                ('retail', 'Retail Pharmacy', 'Standard retail medical shop', 1),
                ('wholesale', 'Wholesale Distributor', 'Bulk medicine distributor', 2),
                ('hospital', 'Hospital Pharmacy', 'In-hospital pharmacy', 3),
                ('clinic', 'Clinic Dispensary', 'Small clinic attached pharmacy', 4),
                ('chain', 'Chain Store', 'Part of a pharmacy chain', 5),
            ]
            for code, name, desc, order in shop_types:
                conn.execute(text("""
                    INSERT INTO shop_type_master (id, code, name, description, is_active, sort_order)
                    VALUES (:id, :code, :name, :desc, true, :order)
                """), {"id": generate_uuid(), "code": code, "name": name, "desc": desc, "order": order})
            print("  Created shop_type_master table and seeded data!")
        else:
            # Check if it has data
            result = conn.execute(text("SELECT COUNT(*) FROM shop_type_master"))
            count = result.scalar()
            if count == 0:
                print("Seeding shop_type_master table...")
                shop_types = [
                    ('retail', 'Retail Pharmacy', 'Standard retail medical shop', 1),
                    ('wholesale', 'Wholesale Distributor', 'Bulk medicine distributor', 2),
                    ('hospital', 'Hospital Pharmacy', 'In-hospital pharmacy', 3),
                    ('clinic', 'Clinic Dispensary', 'Small clinic attached pharmacy', 4),
                    ('chain', 'Chain Store', 'Part of a pharmacy chain', 5),
                ]
                for code, name, desc, order in shop_types:
                    conn.execute(text("""
                        INSERT INTO shop_type_master (id, code, name, description, is_active, sort_order)
                        VALUES (:id, :code, :name, :desc, true, :order)
                    """), {"id": generate_uuid(), "code": code, "name": name, "desc": desc, "order": order})
                print("  Seeded shop_type_master data!")
            else:
                print(f"shop_type_master already has {count} records")
        
        conn.commit()
        
        # Verify data
        print("\n=== Verification ===")
        result = conn.execute(text("SELECT code, name FROM shop_type_master ORDER BY sort_order"))
        rows = result.fetchall()
        print("Shop Types:")
        for row in rows:
            print(f"  {row[0]}: {row[1]}")
        
        result = conn.execute(text("SELECT code, name FROM status_master WHERE entity_type = 'shop' ORDER BY sort_order"))
        rows = result.fetchall()
        print("\nShop Statuses:")
        for row in rows:
            print(f"  {row[0]}: {row[1]}")
        
        print("\nDone! Please refresh the Edit Medical Shop page.")

if __name__ == "__main__":
    main()
