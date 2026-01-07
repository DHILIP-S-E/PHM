"""Check password hashes in database"""
from app.db.database import SessionLocal
from app.db.models import User

db = SessionLocal()
users = db.query(User).all()

print(f"Total users: {len(users)}")
for user in users:
    hash_len = len(user.password_hash) if user.password_hash else 0
    print(f"{user.email}: hash_length={hash_len}")
    if hash_len > 0:
        print(f"  First 10 chars: {user.password_hash[:10]}")
        print(f"  Hash starts with $2b$: {user.password_hash.startswith('$2b$')}")

db.close()
