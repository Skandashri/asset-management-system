"""
Migration script to set up RBAC (Role-Based Access Control) in the database.
Creates default roles and assigns permissions.
"""

import sys
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.models import Role, User, Base
from app.auth import get_password_hash
import uuid

def create_default_roles(db: Session):
    """Create default Admin and Employee roles if they don't exist."""
    
    # Create Admin role with all permissions
    admin_role = db.query(Role).filter(Role.name == "Admin").first()
    if not admin_role:
        admin_role = Role(
            name="Admin",
            permissions=["all"]  # Wildcard for all permissions
        )
        db.add(admin_role)
        print("✓ Created Admin role with full permissions")
    else:
        print("✓ Admin role already exists")
    
    # Create Employee role with limited permissions
    employee_role = db.query(Role).filter(Role.name == "Employee").first()
    if not employee_role:
        employee_role = Role(
            name="Employee",
            permissions=[
                "view:my_gear",      # View own assigned assets
                "view:assets",       # View all inventory (read-only)
            ]
        )
        db.add(employee_role)
        print("✓ Created Employee role with limited permissions")
    else:
        print("✓ Employee role already exists")
    
    db.commit()
    return admin_role, employee_role

def create_or_update_users(db: Session, admin_role: Role, employee_role: Role):
    """Create default users or update existing ones with roles."""
    
    # Create/Update Admin user
    admin_user = db.query(User).filter(User.email == "admin@optiasset.com").first()
    if not admin_user:
        admin_user = User(
            name="System Administrator",
            email="admin@optiasset.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            role_id=admin_role.id
        )
        db.add(admin_user)
        print("✓ Created Admin user (email: admin@optiasset.com, password: admin123)")
    else:
        admin_user.role_id = admin_role.id
        print("✓ Updated Admin user with Admin role")
    
    # Create/Update Employee user
    employee_user = db.query(User).filter(User.email == "employee@optiasset.com").first()
    if not employee_user:
        employee_user = User(
            name="John Employee",
            email="employee@optiasset.com",
            hashed_password=get_password_hash("employee123"),
            is_active=True,
            role_id=employee_role.id
        )
        db.add(employee_user)
        print("✓ Created Employee user (email: employee@optiasset.com, password: employee123)")
    else:
        employee_user.role_id = employee_role.id
        print("✓ Updated Employee user with Employee role")
    
    db.commit()

def run_migration():
    """Run the complete RBAC migration."""
    print("\n🚀 Starting RBAC Migration...\n")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created/verified\n")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Step 1: Create default roles
        print("Step 1: Creating default roles...")
        admin_role, employee_role = create_default_roles(db)
        print()
        
        # Step 2: Create/update users with roles
        print("Step 2: Setting up default users...")
        create_or_update_users(db, admin_role, employee_role)
        print()
        
        print("✅ RBAC Migration completed successfully!\n")
        print("=" * 60)
        print("DEFAULT CREDENTIALS:")
        print("=" * 60)
        print("Admin Login:")
        print("  Email: admin@optiasset.com")
        print("  Password: admin123")
        print("\nEmployee Login:")
        print("  Email: employee@optiasset.com")
        print("  Password: employee123")
        print("=" * 60 + "\n")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Migration failed: {str(e)}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    run_migration()
