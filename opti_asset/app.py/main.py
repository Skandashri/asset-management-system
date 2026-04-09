from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .dependencies import engine
from .routers import employees, assets, assignments

# Explicitly create tables just in case, though usually handled by migrations (Alembic)
models.Base.metadata.create_all(bind=engine)

description = """
# Smart Asset Management System API 🚀

Welcome to the backend API for the Smart Asset Management System. This API provides 
comprehensive tools to manage employees, physical/digital company assets, and track 
asset assignments efficiently.

## Core Features:
* **Employees**: Register, update, and soft-delete personnel records.
* **Assets**: Inventory tracking with availability statuses.
* **Assignments**: Securely check out and return assets enforcing availability rules.

*Designed tightly integrated with PostgreSQL & SQLAlchemy for reliability.*
"""

app = FastAPI(
    title="Smart Asset Management System",
    description=description,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=[
        {
            "name": "Employees",
            "description": "Operations with employees. The **login** logic is outside this scope.",
        },
        {
            "name": "Assets",
            "description": "Manage physical and digital asset inventory.",
        },
        {
            "name": "Assignments",
            "description": "Manage asset checkout and return workflows.",
        },
    ]
)

# -----------------
# CORS Configuration
# -----------------
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    # Add your frontend application origins here
    "*"  # Allows all origins for development (Change in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------
# API Routers Inclusion
# -----------------
app.include_router(employees.router)
app.include_router(assets.router)
app.include_router(assignments.router)

@app.get("/", tags=["Health"])
def root():
    """
    Root endpoint verifying API status.
    """
    return {"message": "Welcome to the Smart Asset Management System API"}
