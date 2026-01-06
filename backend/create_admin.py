"""Create Super Admin User"""
from app.db.database import SessionLocal
from app.db.models import User, RoleType
from app.core.security import get_password_hash

def create_admin():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "admin@pharmaec.com").first()
        if existing:
            print("Admin already exists!")
            return
        
        admin = User(
            email="admin@pharmaec.com",
            password_hash=get_password_hash("admin123"),
            full_name="Super Administrator",
            phone="+91-9876543210",
            role=RoleType.SUPER_ADMIN,
            is_active=True
        )
        db.add(admin)
        db.commit()
        print("=" * 50)
        print("Super Admin created successfully!")
        print("=" * 50)
        print("Email:    admin@pharmaec.com")
        print("Password: admin123")
        print("=" * 50)
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
