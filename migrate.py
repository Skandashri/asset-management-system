import sys
from sqlalchemy import text
from app.database import SessionLocal

db = SessionLocal()
try:
    print("Checking schemas...")
    db.execute(text("ALTER TABLE users ADD COLUMN hashed_password VARCHAR;"))
    db.commit()
    print("Added hashed_password to users")
except Exception as e:
    db.rollback()
    print(f"Error altering users: {e}")

try:
    db.execute(text("ALTER TABLE roles ADD COLUMN permissions VARCHAR[];"))
    db.commit()
    print("Added permissions to roles")
except Exception as e:
    db.rollback()
    print(f"Error altering roles: {e}")

print("Done altering tables.")
db.close()
