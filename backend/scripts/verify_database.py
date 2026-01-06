"""
Database Table Verification Script for PharmaEC Management System
Run this script to check existing tables and create missing ones.

Usage:
    python scripts/verify_database.py
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import inspect, text
from app.db.database import engine, Base
from app.db import models  # noqa: F401 - Import all models


def get_existing_tables():
    """Get list of tables that already exist in the database."""
    inspector = inspect(engine)
    return set(inspector.get_table_names())


def get_model_tables():
    """Get list of tables defined in SQLAlchemy models."""
    return set(Base.metadata.tables.keys())


def check_and_create_tables():
    """Check existing tables and create only missing ones."""
    print("=" * 60)
    print("PharmaEC Database Verification Script")
    print("=" * 60)
    
    # Get existing and expected tables
    existing_tables = get_existing_tables()
    model_tables = get_model_tables()
    
    print(f"\n📊 Tables in SQLAlchemy models: {len(model_tables)}")
    print(f"📊 Tables in database: {len(existing_tables)}")
    
    # Find missing tables
    missing_tables = model_tables - existing_tables
    extra_tables = existing_tables - model_tables - {'alembic_version'}  # Exclude alembic table
    
    print(f"\n✅ Tables already exist: {len(existing_tables & model_tables)}")
    
    if missing_tables:
        print(f"\n⚠️  Missing tables ({len(missing_tables)}):")
        for table in sorted(missing_tables):
            print(f"   - {table}")
        
        # Create only missing tables
        print("\n🔧 Creating missing tables...")
        tables_to_create = [Base.metadata.tables[name] for name in missing_tables]
        Base.metadata.create_all(bind=engine, tables=tables_to_create)
        print("✅ Missing tables created successfully!")
    else:
        print("\n✅ All tables exist! No action needed.")
    
    if extra_tables:
        print(f"\n📝 Extra tables in database (not in models): {len(extra_tables)}")
        for table in sorted(extra_tables):
            print(f"   - {table}")
    
    # Verify final state
    print("\n" + "=" * 60)
    print("FINAL VERIFICATION")
    print("=" * 60)
    
    final_existing = get_existing_tables()
    final_missing = model_tables - final_existing
    
    if not final_missing:
        print(f"✅ All {len(model_tables)} tables verified successfully!")
    else:
        print(f"❌ Still missing {len(final_missing)} tables:")
        for table in sorted(final_missing):
            print(f"   - {table}")
    
    return len(final_missing) == 0


def list_all_tables():
    """List all tables with their column count."""
    print("\n📋 Complete Table List:")
    print("-" * 60)
    
    inspector = inspect(engine)
    existing_tables = sorted(inspector.get_table_names())
    
    for i, table in enumerate(existing_tables, 1):
        columns = inspector.get_columns(table)
        indexes = inspector.get_indexes(table)
        print(f"{i:3}. {table:40} ({len(columns)} cols, {len(indexes)} indexes)")
    
    print("-" * 60)
    print(f"Total: {len(existing_tables)} tables")


if __name__ == "__main__":
    try:
        success = check_and_create_tables()
        list_all_tables()
        
        if success:
            print("\n🎉 Database verification completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Database verification failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
