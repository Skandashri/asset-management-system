"""
Update Employee role permissions to include view:assets
"""
from app.database import SessionLocal
from app.models import Role

db = SessionLocal()

try:
    # Get Employee role
    employee_role = db.query(Role).filter(Role.name == "Employee").first()
    
    if employee_role:
        print(f"Current Employee permissions: {employee_role.permissions}")
        
        # Update permissions
        employee_role.permissions = ["view:my_gear", "view:assets"]
        db.commit()
        
        print(f"Updated Employee permissions: {employee_role.permissions}")
        print("\n✅ Employee role updated!")
    else:
        print("❌ Employee role not found!")
        
finally:
    db.close()
