"""
Migration script to add Super Admin role, secondary role support, and asset reports.
Run this after updating the models.
"""

import sqlite3
from datetime import datetime

def migrate():
    # Connect to database
    conn = sqlite3.connect('test_asset_management.db')
    cursor = conn.cursor()
    
    print("Starting migration...")
    
    try:
        # 1. Add secondary_role_id column to users table
        print("Adding secondary_role_id column to users table...")
        cursor.execute('''
            ALTER TABLE users ADD COLUMN secondary_role_id TEXT
        ''')
        
        # 2. Create asset_reports table
        print("Creating asset_reports table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asset_reports (
                id TEXT PRIMARY KEY,
                asset_id TEXT NOT NULL,
                reported_by_id TEXT NOT NULL,
                report_type TEXT NOT NULL,
                description TEXT NOT NULL,
                severity TEXT DEFAULT 'Medium',
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP,
                admin_notes TEXT,
                FOREIGN KEY (asset_id) REFERENCES assets(id),
                FOREIGN KEY (reported_by_id) REFERENCES users(id)
            )
        ''')
        
        # 3. Create indexes for better performance
        print("Creating indexes...")
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_reports_asset ON asset_reports(asset_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_reports_user ON asset_reports(reported_by_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_reports_status ON asset_reports(status)')
        
        # 4. Check if Super Admin role exists, if not create it
        print("Checking/creating Super Admin role...")
        cursor.execute('SELECT id FROM roles WHERE name = "Super Admin"')
        super_admin = cursor.fetchone()
        
        if not super_admin:
            import uuid
            super_admin_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO roles (id, name, permissions)
                VALUES (?, ?, ?)
            ''', (super_admin_id, 'Super Admin', '["all"]'))
            print(f"Created Super Admin role with ID: {super_admin_id}")
        else:
            print("Super Admin role already exists")
        
        # 5. Update Admin role to include report management permissions
        print("Updating Admin role permissions...")
        cursor.execute('''
            UPDATE roles 
            SET permissions = '["view:assets", "manage:assets", "view:assignments", "manage:assignments", "view:users", "manage:users", "view:dashboard", "view:reports", "manage:reports"]'
            WHERE name = 'Admin'
        ''')
        
        # 6. Create Employee role if it doesn't exist
        print("Checking/creating Employee role...")
        cursor.execute('SELECT id FROM roles WHERE name = "Employee"')
        employee = cursor.fetchone()
        
        if not employee:
            import uuid
            employee_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO roles (id, name, permissions)
                VALUES (?, ?, ?)
            ''', (employee_id, 'Employee', '["view:assets", "view:assignments", "view:dashboard", "create:reports", "view:my_reports"]'))
            print(f"Created Employee role with ID: {employee_id}")
        else:
            print("Employee role already exists")
        
        # 7. Create default Super Admin user
        print("Creating default Super Admin account...")
        cursor.execute('SELECT id FROM users WHERE email = "superadmin@optiasset.com"')
        superadmin_user = cursor.fetchone()
        
        if not superadmin_user:
            import uuid
            import hashlib
            
            # Get Super Admin role ID
            cursor.execute('SELECT id FROM roles WHERE name = "Super Admin"')
            super_admin_role = cursor.fetchone()
            
            if super_admin_role:
                superadmin_id = str(uuid.uuid4())
                # Hash password: admin123
                hashed_pwd = hashlib.sha256("superadmin123".encode()).hexdigest()
                
                cursor.execute('''
                    INSERT INTO users (id, role_id, name, email, hashed_password, is_active, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
                ''', (superadmin_id, super_admin_role[0], 'Super Administrator', 'superadmin@optiasset.com', hashed_pwd, True))
                print(f"✅ Created Super Admin user: superadmin@optiasset.com / superadmin123")
            else:
                print("⚠️  Could not create Super Admin - role not found")
        else:
            print("Super Admin user already exists")
        
        # 8. Update existing Admin password for consistency
        print("Updating default Admin credentials...")
        cursor.execute('SELECT id FROM users WHERE email = "admin@optiasset.com"')
        admin_user = cursor.fetchone()
        
        if admin_user:
            import hashlib
            hashed_pwd = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute('''
                UPDATE users SET hashed_password = ? WHERE email = "admin@optiasset.com"
            ''', (hashed_pwd,))
            print("✅ Admin password confirmed: admin@optiasset.com / admin123")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")
        print("\nNew Features Added:")
        print("- Secondary role support for role switching")
        print("- Asset Reports system for damaged/lost items")
        print("- Super Admin role hierarchy")
        print("- Enhanced Admin permissions for report management")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Migration failed: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
