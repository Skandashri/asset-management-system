"""
Script to demonstrate soft delete (deactivation) functionality
This shows the is_active flag being set to False instead of hard deleting records
"""

from app.database import SessionLocal
from app.models import User, Asset, Assignment
from datetime import datetime

def demonstrate_deactivation():
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("DEMONSTRATING SOFT DELETE / DEACTIVATION")
        print("=" * 80)
        
        # 1. Deactivate a user (Frank Miller)
        print("\n👤 DEACTIVATING USER: Frank Miller")
        print("-" * 80)
        
        frank = db.query(User).filter(User.email == "frank@company.com").first()
        if frank:
            print(f"Before: {frank.name} - Active: {frank.is_active}")
            
            # Soft delete by setting is_active = False
            frank.is_active = False
            
            db.commit()
            print(f"After:  {frank.name} - Active: {frank.is_active}")
            print("✅ User Frank Miller deactivated (soft deleted)")
        else:
            print("❌ User Frank Miller not found")
        
        # 2. Deactivate an asset (iPhone)
        print("\n\n💼 DEACTIVATING ASSET: iPhone 13 Pro")
        print("-" * 80)
        
        iphone = db.query(Asset).filter(Asset.asset_tag == "IPHONE-13-001").first()
        if iphone:
            print(f"Before: {iphone.name} - Status: {iphone.status} - Active: {iphone.is_active}")
            
            # Soft delete by setting is_active = False
            iphone.is_active = False
            
            db.commit()
            print(f"After:  {iphone.name} - Status: {iphone.status} - Active: {iphone.is_active}")
            print("✅ Asset iPhone 13 Pro deactivated (soft deleted)")
        else:
            print("❌ Asset iPhone 13 Pro not found")
        
        # 3. Show remaining active records
        print("\n\n📊 CURRENT DATABASE STATE")
        print("=" * 80)
        
        active_users = db.query(User).filter(User.is_active == True).count()
        inactive_users = db.query(User).filter(User.is_active == False).count()
        total_users = db.query(User).count()
        
        active_assets = db.query(Asset).filter(Asset.is_active == True).count()
        inactive_assets = db.query(Asset).filter(Asset.is_active == False).count()
        total_assets = db.query(Asset).count()
        
        print(f"\nUSERS:")
        print(f"  Total: {total_users}")
        print(f"  Active: {active_users} ✅")
        print(f"  Inactive (Deactivated): {inactive_users} ❌")
        
        print(f"\nASSETS:")
        print(f"  Total: {total_assets}")
        print(f"  Active: {active_assets} ✅")
        print(f"  Inactive (Deactivated): {inactive_assets} ❌")
        
        # 4. Show which users are deactivated
        print("\n\n📋 DEACTIVATED USERS LIST:")
        print("-" * 80)
        inactive_user_list = db.query(User).filter(User.is_active == False).all()
        for user in inactive_user_list:
            print(f"  ❌ {user.name} ({user.email}) - Deactivated at: {user.created_at}")
        
        # 5. Show which assets are deactivated
        print("\n\n📋 DEACTIVATED ASSETS LIST:")
        print("-" * 80)
        inactive_asset_list = db.query(Asset).filter(Asset.is_active == False).all()
        for asset in inactive_asset_list:
            print(f"  ❌ {asset.asset_tag} - {asset.name} - Status: {asset.status}")
        
        # 6. Show active users only (what API returns by default)
        print("\n\n✅ ACTIVE USERS ONLY (API Default Query):")
        print("-" * 80)
        active_user_list = db.query(User).filter(User.is_active == True).all()
        for user in active_user_list:
            print(f"  ✅ {user.name} ({user.email}) - Role: {user.role.name if user.role else 'None'}")
        
        # 7. Show active assets only
        print("\n\n✅ ACTIVE ASSETS ONLY (API Default Query):")
        print("-" * 80)
        active_asset_list = db.query(Asset).filter(Asset.is_active == True).all()
        for asset in active_asset_list:
            status_emoji = "🟢" if asset.status == "Available" else "🔵"
            print(f"  {status_emoji} {asset.asset_tag} - {asset.name} [{asset.status}]")
        
        print("\n" + "=" * 80)
        print("💡 KEY POINTS ABOUT SOFT DELETE:")
        print("=" * 80)
        print("1. Records are NOT deleted from database")
        print("2. is_active flag set to FALSE instead")
        print("3. API filters out inactive records by default")
        print("4. Historical data preserved for audit trails")
        print("5. Can be reactivated by setting is_active = TRUE")
        print("=" * 80)
        
        # 8. Reactivation example (optional)
        print("\n\n🔄 DEMONSTRATING REACTIVATION:")
        print("-" * 80)
        
        # Ask user if they want to reactivate
        choice = input("Reactivate Frank Miller? (y/n): ").lower().strip()
        if choice == 'y':
            frank.is_active = True
            db.commit()
            print(f"✅ Frank Miller reactivated! is_active: {frank.is_active}")
        else:
            print("ℹ️  Frank Miller remains deactivated")
        
        print("\n" + "=" * 80)
        print("✅ Deactivation demonstration complete!")
        print("=" * 80)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error occurred: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    demonstrate_deactivation()
