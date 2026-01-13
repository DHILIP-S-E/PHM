"""
Script to add missing entity statuses to status_master table
Run this to fix the Edit Medical Shop form dropdowns not loading
"""
import uuid
import sys
import os

# Add the app directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.config import settings

def main():
    print(f"Connecting to database...")
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        # Check current status_master contents
        print("Current entity types in status_master:")
        result = conn.execute(text("SELECT DISTINCT entity_type FROM status_master"))
        existing_types = [row[0] for row in result.fetchall()]
        print(f"  {existing_types}")
        
        # Define statuses to add for each entity type
        statuses_to_add = {
            'shop': [
                ('active', 'Active', 'green', False, True, 1),
                ('inactive', 'Inactive', 'gray', False, False, 2),
                ('suspended', 'Suspended', 'orange', False, False, 3),
                ('closed', 'Permanently Closed', 'red', True, False, 4),
            ],
            'warehouse': [
                ('active', 'Active', 'green', False, True, 1),
                ('inactive', 'Inactive', 'gray', False, False, 2),
                ('maintenance', 'Under Maintenance', 'orange', False, False, 3),
                ('closed', 'Permanently Closed', 'red', True, False, 4),
            ],
            'user': [
                ('active', 'Active', 'green', False, True, 1),
                ('inactive', 'Inactive', 'gray', False, False, 2),
                ('suspended', 'Suspended', 'orange', False, False, 3),
                ('terminated', 'Terminated', 'red', True, False, 4),
            ],
            'medicine': [
                ('active', 'Active', 'green', False, True, 1),
                ('inactive', 'Inactive', 'gray', False, False, 2),
                ('discontinued', 'Discontinued', 'red', True, False, 3),
            ],
        }
        
        # Insert missing statuses
        for entity_type, statuses in statuses_to_add.items():
            # Check if entity type already has statuses
            result = conn.execute(text("SELECT COUNT(*) FROM status_master WHERE entity_type = :entity_type"), {"entity_type": entity_type})
            count = result.scalar()
            
            if count > 0:
                print(f"  Skipping {entity_type} - already has {count} statuses")
                continue
            
            print(f"  Adding statuses for '{entity_type}'...")
            for code, name, color, is_terminal, is_default, sort_order in statuses:
                conn.execute(text("""
                    INSERT INTO status_master (id, entity_type, code, name, color, is_terminal, is_default, is_active, sort_order)
                    VALUES (:id, :entity_type, :code, :name, :color, :is_terminal, :is_default, :is_active, :sort_order)
                """), {
                    "id": str(uuid.uuid4()),
                    "entity_type": entity_type,
                    "code": code,
                    "name": name,
                    "color": color,
                    "is_terminal": is_terminal,
                    "is_default": is_default,
                    "is_active": True,
                    "sort_order": sort_order
                })
            
            print(f"    Added {len(statuses)} statuses for {entity_type}")
        
        conn.commit()
        print("\nDone! Please restart the backend server and refresh the frontend.")

if __name__ == "__main__":
    main()
