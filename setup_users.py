"""
Add missing Admin role and create users
"""
import sys
sys.path.append('app')

from app import models, auth
from sqlalchemy.orm import Session
from app.database import SessionLocal

db = SessionLocal()

try:
    # Check for Admin role
    admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
    if not admin_role:
        print("Creating Admin role...")
        admin_role = models.Role(
            name="Admin",
            permissions=["all"]
        )
        db.add(admin_role)
        db.commit()
        print(f"✅ Created Admin role with ID: {admin_role.id}")
    else:
        print(f"✅ Admin role exists with ID: {admin_role.id}")
    
    # Check for Super Admin role
    super_admin_role = db.query(models.Role).filter(models.Role.name == "Super Admin").first()
    if not super_admin_role:
        print("Creating Super Admin role...")
        super_admin_role = models.Role(
            name="Super Admin",
            permissions=["all"]  # Same permissions as Admin
        )
        db.add(super_admin_role)
        db.commit()
        print(f"✅ Created Super Admin role with ID: {super_admin_role.id}")
    else:
        print(f"✅ Super Admin role exists with ID: {super_admin_role.id}")
        # Ensure Super Admin has ["all"] permissions
        if "all" not in super_admin_role.permissions:
            print("Updating Super Admin permissions to include ['all']...")
            super_admin_role.permissions = ["all"]
            db.commit()
            print("✅ Updated Super Admin permissions")
    
    # Check for Employee role
    employee_role = db.query(models.Role).filter(models.Role.name == "Employee").first()
    if not employee_role:
        print("Creating Employee role...")
        employee_role = models.Role(
            name="Employee",
            permissions=["view:assets", "view:assignments"]
        )
        db.add(employee_role)
        db.commit()
        print(f"✅ Created Employee role with ID: {employee_role.id}")
    else:
        print(f"✅ Employee role exists with ID: {employee_role.id}")
    
    # Create users
    users_data = [
        ("superadmin@optiasset.com", "Super Administrator", "superadmin123", super_admin_role.id),
        ("admin@optiasset.com", "Admin User", "admin123", admin_role.id),
        ("employee@optiasset.com", "Employee User", "employee123", employee_role.id),
    ]
    
    for email, name, password, role_id in users_data:
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            user = models.User(
                name=name,
                email=email,
                hashed_password=auth.get_password_hash(password),
                role_id=role_id,
                is_active=True
            )
            db.add(user)
            print(f"✅ Created {name}: {email} / {password}")
        else:
            user.hashed_password = auth.get_password_hash(password)
            print(f"✅ Updated {name} password: {email} / {password}")
    
    db.commit()
    print("\n🎉 All users ready!")
    print("\n📝 Login Credentials:")
    print("   Super Admin: superadmin@optiasset.com / superadmin123")
    print("   Admin: admin@optiasset.com / admin123")
    print("   Employee: employee@optiasset.com / employee123")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
