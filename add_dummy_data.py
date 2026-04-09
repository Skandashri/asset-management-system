"""
Script to add dummy data to all database tables for testing
Run this to populate your database with sample records
"""

from app.database import SessionLocal
from app.models import Role, User, Asset, Assignment, AssetStatusLog
from app.auth import get_password_hash
from datetime import datetime, timedelta
import uuid

from app.database import SessionLocal, engine
from app.models import Role, User, Asset, Assignment, AssetStatusLog, Base

def add_dummy_data():
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("ADDING DUMMY DATA TO DATABASE")
        print("=" * 80)
        
        # Check if roles exist, create if not
        super_admin_role = db.query(Role).filter(Role.name == "Super Admin").first()
        admin_role = db.query(Role).filter(Role.name == "Admin").first()
        employee_role = db.query(Role).filter(Role.name == "Employee").first()
        
        if not super_admin_role:
            super_admin_role = Role(name="Super Admin", permissions=["all"])
            db.add(super_admin_role)
            print("✅ Created Super Admin role")

        if not admin_role:
            admin_role = Role(name="Admin", permissions=["view:assets", "manage:assets", "view:assignments", "manage:assignments", "view:users", "manage:users", "view:dashboard", "view:reports", "manage:reports"])
            db.add(admin_role)
            print("✅ Created Admin role")
        
        if not employee_role:
            employee_role = Role(name="Employee", permissions=["view:assets", "view:assignments", "view:dashboard", "create:reports", "view:my_reports"])
            db.add(employee_role)
            print("✅ Created Employee role")
        
        db.commit()
        
        # Add more users
        dummy_users = [
            {"name": "Super Administrator", "email": "superadmin@optiasset.com", "role_id": super_admin_role.id},
            {"name": "Admin User", "email": "admin@optiasset.com", "role_id": admin_role.id},
            {"name": "Alice Johnson", "email": "alice@company.com", "role_id": employee_role.id},
            {"name": "Bob Smith", "email": "bob@company.com", "role_id": employee_role.id},
            {"name": "Carol Williams", "email": "carol@company.com", "role_id": employee_role.id},
            {"name": "David Brown", "email": "david@company.com", "role_id": employee_role.id},
            {"name": "Eve Davis", "email": "eve@company.com", "role_id": employee_role.id},
            {"name": "Frank Miller", "email": "frank@company.com", "role_id": employee_role.id},
        ]
        
        for user_data in dummy_users:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                new_user = User(
                    name=user_data["name"],
                    email=user_data["email"],
                    hashed_password=get_password_hash("password123"),
                    is_active=True,
                    role_id=user_data["role_id"]
                )
                db.add(new_user)
                print(f"✅ Created user: {user_data['name']} ({user_data['email']})")
        
        db.commit()
        
        # Add more assets
        dummy_assets = [
            {"asset_tag": "LAPTOP-HP-001", "name": "HP EliteBook 840 G8"},
            {"asset_tag": "LAPTOP-LEN-002", "name": "Lenovo ThinkPad X1 Carbon"},
            {"asset_tag": "MONITOR-DELL-001", "name": "Dell UltraSharp 27\" U2720Q"},
            {"asset_tag": "MONITOR-LG-002", "name": "LG 27\" 4K UHD Monitor"},
            {"asset_tag": "KEYBOARD-LOGI-001", "name": "Logitech MX Keys Keyboard"},
            {"asset_tag": "MOUSE-LOGI-001", "name": "Logitech MX Master 3 Mouse"},
            {"asset_tag": "CHAIR-HERMAN-001", "name": "Herman Miller Aeron Chair"},
            {"asset_tag": "DESK-STAND-001", "name": "Standing Desk Electric 48\""},
            {"asset_tag": "IPAD-PRO-001", "name": "iPad Pro 12.9\" M1"},
            {"asset_tag": "IPHONE-13-001", "name": "iPhone 13 Pro 256GB"},
            {"asset_tag": "WEBCAM-LOGI-001", "name": "Logitech Brio 4K Webcam"},
            {"asset_tag": "HEADSET-SONY-001", "name": "Sony WH-1000XM4 Headphones"},
        ]
        
        created_assets = []
        for asset_data in dummy_assets:
            existing = db.query(Asset).filter(Asset.asset_tag == asset_data["asset_tag"]).first()
            if not existing:
                new_asset = Asset(
                    asset_tag=asset_data["asset_tag"],
                    name=asset_data["name"],
                    status="Available",
                    is_active=True
                )
                db.add(new_asset)
                created_assets.append(new_asset)
                print(f"✅ Created asset: {asset_data['asset_tag']} - {asset_data['name']}")
        
        db.commit()
        
        # Get all employees and available assets
        employees = db.query(User).filter(User.role_id == employee_role.id).limit(5).all()
        available_assets = db.query(Asset).filter(Asset.status == "Available").limit(5).all()
        
        # Create some assignments
        print("\n📦 Creating assignments...")
        for i in range(min(len(employees), len(available_assets))):
            employee = employees[i]
            asset = available_assets[i]
            
            # Check if already assigned
            existing = db.query(Assignment).filter(
                Assignment.asset_id == asset.id,
                Assignment.return_date == None
            ).first()
            
            if not existing:
                # Create assignment
                assigned_date = datetime.utcnow() - timedelta(days=30-i*5)
                new_assignment = Assignment(
                    user_id=employee.id,
                    asset_id=asset.id,
                    assigned_date=assigned_date,
                    return_date=None
                )
                db.add(new_assignment)
                
                # Update asset status
                asset.status = "Assigned"
                
                # Create status log
                status_log = AssetStatusLog(
                    asset_id=asset.id,
                    old_status="Available",
                    new_status="Assigned",
                    changed_at=assigned_date
                )
                db.add(status_log)
                
                print(f"✅ Assigned {asset.name} to {employee.name}")
        
        db.commit()
        
        # Print summary
        total_roles = db.query(Role).count()
        total_users = db.query(User).count()
        total_assets = db.query(Asset).count()
        total_assignments = db.query(Assignment).count()
        active_assignments = db.query(Assignment).filter(Assignment.return_date == None).count()
        
        print("\n" + "=" * 80)
        print("📊 DATABASE SUMMARY")
        print("=" * 80)
        print(f"Total Roles: {total_roles}")
        print(f"Total Users: {total_users}")
        print(f"Total Assets: {total_assets}")
        print(f"Total Assignments: {total_assignments}")
        print(f"Active Assignments: {active_assignments}")
        print("=" * 80)
        
        print("\n✅ Dummy data added successfully!")
        print("\n💡 Test Credentials:")
        print("   Admin: admin@optiasset.com / admin123")
        print("   Employee: employee@optiasset.com / employee123")
        print("   Any dummy user: alice@company.com / password123")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error occurred: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_dummy_data()
