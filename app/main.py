from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text

from app import models
from app.database import engine
from app.routers import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initializing all declarative models bound exactly
    try:
        models.Base.metadata.create_all(bind=engine)
        print("Database tables structurally bound and validated natively.")
        
        # Add missing columns to users table if they don't exist (for production Supabase)
        try:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN department VARCHAR;"))
                conn.commit()
        except Exception:
            pass
            
        try:
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE users ADD COLUMN contact VARCHAR;"))
                conn.commit()
        except Exception:
            pass
        
        # Seed initial roles and users on startup
        from app.database import SessionLocal
        from app.auth import get_password_hash
        db = SessionLocal()
        try:
            # Create Super Admin role if it doesn't exist
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
                print(f"✅ Created Super Admin role")
            
            # Create Admin role if it doesn't exist
            admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
            if not admin_role:
                print("Creating Admin role...")
                admin_role = models.Role(
                    name="Admin",
                    permissions=["all"]
                )
                db.add(admin_role)
                db.commit()
                db.refresh(admin_role)
                print(f"✅ Created Admin role")
                
            # Create Employee role if it doesn't exist
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
                print(f"✅ Created Employee role")
                
            # Create Super Admin user if it doesn't exist
            superadmin_user = db.query(models.User).filter(models.User.email == "superadmin@optiasset.com").first()
            if not superadmin_user:
                print("Creating Super Admin user...")
                superadmin_user = models.User(
                    name="Super Administrator",
                    email="superadmin@optiasset.com",
                    hashed_password=get_password_hash("superadmin123"),
                    role_id=super_admin_role.id,
                    is_active=True
                )
                db.add(superadmin_user)
                db.commit()
                print(f"✅ Created Super Admin user with role_id: {super_admin_role.id}")
                print("   Email: superadmin@optiasset.com")
                print("   Password: superadmin123")
            else:
                # Ensure Super Admin has the correct role and is active
                print(f"Super Admin user exists, verifying role...")
                print(f"   Current role_id: {superadmin_user.role_id}")
                print(f"   Expected role_id: {super_admin_role.id}")
                if superadmin_user.role_id != super_admin_role.id:
                    print("   Updating Super Admin role...")
                    superadmin_user.role_id = super_admin_role.id
                    db.commit()
                if not superadmin_user.is_active:
                    print("   Reactivating Super Admin account...")
                    superadmin_user.is_active = True
                    db.commit()
                # Update password to ensure it's correct
                superadmin_user.hashed_password = get_password_hash("superadmin123")
                db.commit()
                print("✅ Super Admin user verified and updated")
            
            # Create Admin user if it doesn't exist
            admin_user = db.query(models.User).filter(models.User.email == "admin@optiasset.com").first()
            if not admin_user:
                print("Creating Admin user...")
                admin_user = models.User(
                    name="OptiAsset Admin",
                    email="admin@optiasset.com",
                    hashed_password=get_password_hash("admin123"),
                    role_id=admin_role.id,
                    is_active=True
                )
                db.add(admin_user)
                db.commit()
                print("✅ Created Admin user: admin@optiasset.com / admin123")
                
            # Create Employee user if it doesn't exist
            employee_user = db.query(models.User).filter(models.User.email == "employee@optiasset.com").first()
            if not employee_user:
                print("Creating Employee user...")
                employee_user = models.User(
                    name="Standard Employee",
                    email="employee@optiasset.com",
                    hashed_password=get_password_hash("employee123"),
                    role_id=employee_role.id,
                    is_active=True
                )
                db.add(employee_user)
                db.commit()
                print("✅ Created Employee user: employee@optiasset.com / employee123")
                
            print("\n🎉 Default users are ready!")
            print("📝 Login Credentials:")
            print("   Super Admin: superadmin@optiasset.com / superadmin123")
            print("   Admin: admin@optiasset.com / admin123")
            print("   Employee: employee@optiasset.com / employee123")
        except Exception as e:
            print(f"Warning: Could not seed initial users. Error: {e}")
            db.rollback()
        finally:
            db.close()
            
    except Exception as e:
        print(f"Warning: Could not connect to database on startup. Error: {e}")
    yield

description = """
# Professional Asset Management System API 🚀 (Advanced)

## Core Features
1. **Users & Roles:** Managed entities formally restricted logically.
2. **Assets:** Control inventory with status mapping conceptually strictly.
3. **Assignments:** Secure mathematically bounded transactional logic mapping conceptually natively organically bound limits natively structurally.
4. **Dashboards:** Metrics intuitively inherently bounds explicitly logically formal statically matches.
"""

app = FastAPI(
    title="Smart Asset Management System API",
    description=description,
    version="1.1.0",
    lifespan=lifespan,
    contact={
        "name": "API Author",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000", 
        "https://optiasset.vercel.app",
        "https://asset-management-system-1-cm2v.onrender.com",
        "*"  # Allow all origins for development (restrict in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Health"])
def root():
    """
    Health check.
    """
    return {"message": "Welcome to the Smart Asset Management API"}

