"""
Script to check and verify master data in the database
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text, inspect
from app.core.config import settings

def main():
    print(f"Connecting to database...")
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # First, let's check which tables exist
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print("\n=== Existing Tables ===")
        master_tables = [t for t in tables if 'master' in t.lower()]
        print(f"  Master tables: {master_tables}")
        
        # Check if shop_type_master table exists
        if 'shop_type_master' in tables:
            print("\n=== Shop Types ===")
            result = conn.execute(text("SELECT id, code, name, is_active FROM shop_type_master ORDER BY sort_order"))
            rows = result.fetchall()
            if rows:
                for row in rows:
                    print(f"  {row}")
            else:
                print("  No shop types found!")
        else:
            print("\n=== Shop Types ===")
            print("  Table 'shop_type_master' does not exist!")
        
        # Check warehouses
        if 'warehouses' in tables:
            print("\n=== Warehouses ===")
            result = conn.execute(text("SELECT id, name, code, status FROM warehouses LIMIT 10"))
            rows = result.fetchall()
            if rows:
                for row in rows:
                    print(f"  {row}")
            else:
                print("  No warehouses found!")
        else:
            print("\n=== Warehouses ===")
            print("  Table 'warehouses' does not exist!")
        
        # Check status_master table
        if 'status_master' in tables:
            print("\n=== Shop Statuses ===")
            result = conn.execute(text("SELECT id, code, name, color FROM status_master WHERE entity_type = 'shop' ORDER BY sort_order"))
            rows = result.fetchall()
            if rows:
                for row in rows:
                    print(f"  {row}")
            else:
                print("  No shop statuses found!")
            
            print("\n=== All Entity Types in status_master ===")
            result = conn.execute(text("SELECT DISTINCT entity_type FROM status_master ORDER BY entity_type"))
            rows = result.fetchall()
            for row in rows:
                print(f"  {row[0]}")
        else:
            print("\n=== Status Master ===")
            print("  Table 'status_master' does not exist!")

if __name__ == "__main__":
    main()
