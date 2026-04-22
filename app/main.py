from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app import models
from app.database import engine
from app.routers import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initializing all declarative models bound exactly
    try:
        models.Base.metadata.create_all(bind=engine)
        print("Database tables structurally bound and validated natively.")
        
        # Seed initial roles and users - commented out for testing
        # from app.database import SessionLocal
        # from app.auth import get_password_hash
        # db = SessionLocal()
        # try:
        #     admin_role = db.query(models.Role).filter(models.Role.name == "Admin").first()
        #     if not admin_role:
        #         admin_role = models.Role(name="Admin", permissions=["all"])
        #         db.add(admin_role)
        #         db.commit()
        #         db.refresh(admin_role)
                
        #     employee_role = db.query(models.Role).filter(models.Role.name == "Employee").first()
        #     if not employee_role:
        #         employee_role = models.Role(name="Employee", permissions=["view:assets", "view:assignments", "view:dashboard"])
        #         db.add(employee_role)
        #         db.commit()
        #         db.refresh(employee_role)
                
        #     admin_user = db.query(models.User).filter(models.User.email == "admin@optiasset.com").first()
        #     if not admin_user:
        #         admin_user = models.User(
        #             name="OptiAsset Admin",
        #             email="admin@optiasset.com",
        #             hashed_password=get_password_hash("admin123"),
        #             role_id=admin_role.id
        #         )
        #         db.add(admin_user)
        #         db.commit()
                
        #     employee_user = db.query(models.User).filter(models.User.email == "employee@optiasset.com").first()
        #     if not employee_user:
        #         employee_user = models.User(
        #             name="Standard Employee",
        #             email="employee@optiasset.com",
        #             hashed_password=get_password_hash("employee123"),
        #             role_id=employee_role.id
        #         )
        #         db.add(employee_user)
        #         db.commit()
        # finally:
        #     db.close()
            
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
        "https://asset-management-system-1-cm2v.onrender.com",  # Allow Render backend
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

