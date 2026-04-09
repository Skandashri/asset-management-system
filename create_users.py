"""
Create default users with proper password hashing using bcrypt
"""
import sys
sys.path.append('app')

from app import models, auth
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Check if Super Admin role exists
    super_admin_role = db.query(models.Role).filter(models.Role.name == "Super Admin").first()
    if not super_admin_role:
        print("Creating Super Admin role...")
        super_admin_role = models.Role(
            name="Super Admin",
            permissions=["all"]
        )
        db.add(super_admin_role)
        db.commit()
        db.refresh(super_admin_role)
        print(f"✅ Created Super Admin role with ID: {super_admin_role.id}")
    else:
        print(f"✅ Super Admin role exists with ID: {super_admin_role.id}")
    
    # Check if Employee role exists
    employee_role = db.query(models.Role).filter(models.Role.name == "Employee").first()
    if not employee_role:
        print("Creating Employee role...")
        employee_role = models.Role(
            name="Employee",
            permissions=["view:assets", "view:assignments", "view:dashboard", "create:reports", "view:my_reports"]
        )
        db.add(employee_role)
        db.commit()
        db.refresh(employee_role)
        print(f"✅ Created Employee role with ID: {employee_role.id}")
    else:
        print(f"✅ Employee role exists with ID: {employee_role.id}")
    
    # Create Super Admin user
    print("\nCreating Super Admin user...")
    superadmin = db.query(models.User).filter(models.User.email == "superadmin@optiasset.com").first()
    if not superadmin:
        hashed_password = auth.get_password_hash("superadmin123")
        superadmin = models.User(
            name="Super Administrator",
            email="superadmin@optiasset.com",
            hashed_password=hashed_password,
            role_id=super_admin_role.id,
            is_active=True
        )
        db.add(superadmin)
        db.commit()
        print("✅ Created Super Admin user:")
        print("   Email: superadmin@optiasset.com")
        print("   Password: superadmin123")
    else:
        print("⚠️  Super Admin user already exists, updating password...")
        superadmin.hashed_password = auth.get_password_hash("superadmin123")
        db.commit()
        print("✅ Updated Super Admin password")
    
    # Update Admin user password
    print("\nUpdating Admin user password...")
    admin_user = db.query(models.User).filter(models.User.email == "admin@optiasset.com").first()
    if admin_user:
        admin_user.hashed_password = auth.get_password_hash("admin123")
        db.commit()
        print("✅ Updated Admin password to: admin123")
    else:
        print("⚠️  Admin user not found")
    
    # Update Employee user password
    print("\nUpdating Employee user password...")
    employee_user = db.query(models.User).filter(models.User.email == "employee@optiasset.com").first()
    if employee_user:
        employee_user.hashed_password = auth.get_password_hash("employee123")
        db.commit()
        print("✅ Updated Employee password to: employee123")
    else:
        print("⚠️  Employee user not found")
    
    print("\n🎉 All users created/updated successfully!")
    print("\n📝 Login Credentials:")
    print("   Super Admin: superadmin@optiasset.com / superadmin123")
    print("   Admin: admin@optiasset.com / admin123")
    print("   Employee: employee@optiasset.com / employee123")
    
finally:
    db.close()
