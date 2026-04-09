"""
Quick script to view all database tables and their contents
Run this to see your actual database state
"""

from app.database import SessionLocal
from app.models import Role, User, Asset, Assignment, AssetStatusLog

def view_database():
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("DATABASE OVERVIEW - OptiAsset Management System")
        print("=" * 80)
        
        # 1. ROLES TABLE
        print("\n\n📋 TABLE: roles")
        print("-" * 80)
        roles = db.query(Role).all()
        print(f"Total Records: {len(roles)}\n")
        for role in roles:
            print(f"ID: {role.id}")
            print(f"Name: {role.name}")
            print(f"Permissions: {role.permissions}")
            print("-" * 80)
        
        # 2. USERS TABLE
        print("\n\n👥 TABLE: users")
        print("-" * 80)
        users = db.query(User).all()
        print(f"Total Records: {len(users)}\n")
        for user in users:
            print(f"ID: {user.id}")
            print(f"Name: {user.name}")
            print(f"Email: {user.email}")
            print(f"Role ID: {user.role_id}")
            print(f"Is Active: {user.is_active}")
            print(f"Created: {user.created_at}")
            if user.role:
                print(f"Role Name: {user.role.name}")
            print("-" * 80)
        
        # 3. ASSETS TABLE
        print("\n\n💼 TABLE: assets")
        print("-" * 80)
        assets = db.query(Asset).all()
        print(f"Total Records: {len(assets)}\n")
        for asset in assets:
            print(f"ID: {asset.id}")
            print(f"Asset Tag: {asset.asset_tag}")
            print(f"Name: {asset.name}")
            print(f"Status: {asset.status}")
            print(f"Is Active: {asset.is_active}")
            print(f"Created: {asset.created_at}")
            print("-" * 80)
        
        # 4. ASSIGNMENTS TABLE
        print("\n\n📦 TABLE: assignments")
        print("-" * 80)
        assignments = db.query(Assignment).all()
        print(f"Total Records: {len(assignments)}\n")
        for assignment in assignments:
            print(f"ID: {assignment.id}")
            print(f"User ID: {assignment.user_id}")
            print(f"Asset ID: {assignment.asset_id}")
            print(f"Assigned Date: {assignment.assigned_date}")
            print(f"Return Date: {assignment.return_date or 'NOT RETURNED'}")
            if assignment.user:
                print(f"User Name: {assignment.user.name}")
            if assignment.asset:
                print(f"Asset Tag: {assignment.asset.asset_tag}")
            print("-" * 80)
        
        # 5. ASSET STATUS LOGS TABLE
        print("\n\n📝 TABLE: asset_status_logs")
        print("-" * 80)
        logs = db.query(Assignment).all()  # Note: Query status logs if needed
        print(f"Total Records: {len(logs)}")
        print("(Status logs track asset status changes automatically)")
        print("-" * 80)
        
        # SUMMARY
        print("\n\n📊 DATABASE SUMMARY")
        print("=" * 80)
        print(f"Total Roles: {len(roles)}")
        print(f"Total Users: {len(users)}")
        print(f"Total Assets: {len(assets)}")
        print(f"Total Assignments: {len(assignments)}")
        print("=" * 80)
        
        # QUICK STATS
        active_users = db.query(User).filter(User.is_active == True).count()
        inactive_users = db.query(User).filter(User.is_active == False).count()
        available_assets = db.query(Asset).filter(Asset.status == "Available").count()
        assigned_assets = db.query(Asset).filter(Asset.status == "Assigned").count()
        
        print("\n📈 QUICK STATS:")
        print(f"Active Users: {active_users}")
        print(f"Inactive Users: {inactive_users}")
        print(f"Available Assets: {available_assets}")
        print(f"Assigned Assets: {assigned_assets}")
        print("=" * 80)
        
    finally:
        db.close()

if __name__ == "__main__":
    view_database()
