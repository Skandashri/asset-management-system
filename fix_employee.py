"""
Fix employee password issue
"""
from app.database import SessionLocal
from app.models import User, Role
from app.auth import get_password_hash

db = SessionLocal()

try:
    # Get Employee role
    employee_role = db.query(Role).filter(Role.name == "Employee").first()
    if not employee_role:
        print("Creating Employee role...")
        employee_role = Role(
            name="Employee",
            permissions=["view:my_gear", "view:assets"]
        )
        db.add(employee_role)
        db.commit()
        employee_role = db.query(Role).filter(Role.name == "Employee").first()
    
    print(f"Employee Role ID: {employee_role.id}")
    print(f"Permissions: {employee_role.permissions}")
    
    # Delete existing employee user
    existing_employee = db.query(User).filter(User.email == "employee@optiasset.com").first()
    if existing_employee:
        db.delete(existing_employee)
        db.commit()
        print("Deleted existing employee user")
    
    # Create new employee user with correct password
    new_employee = User(
        name="John Employee",
        email="employee@optiasset.com",
        hashed_password=get_password_hash("employee123"),
        is_active=True,
        role_id=employee_role.id
    )
    db.add(new_employee)
    db.commit()
    
    print("\n✅ Employee user recreated successfully!")
    print(f"Email: employee@optiasset.com")
    print(f"Password: employee123")
    
    # Verify the password works
    from app import auth
    test = auth.verify_password('employee123', new_employee.hashed_password)
    print(f"\nPassword verification test: {test}")
    
finally:
    db.close()
