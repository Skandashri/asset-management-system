"""
Script to update admin and employee passwords to match login page defaults
"""

from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash

def update_passwords():
    db = SessionLocal()

    try:
        # Update admin password
        admin_user = db.query(User).filter(User.email == "admin@optiasset.com").first()
        if admin_user:
            admin_user.hashed_password = get_password_hash("admin123")
            print("✅ Updated admin password")

        # Update employee password
        employee_user = db.query(User).filter(User.email == "employee@optiasset.com").first()
        if employee_user:
            employee_user.hashed_password = get_password_hash("employee123")
            print("✅ Updated employee password")

        db.commit()
        print("✅ Passwords updated successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_passwords()