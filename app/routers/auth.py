from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, auth
from app.dependencies import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=dict)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # Debug logging
    print(f"\n=== Login Attempt ===")
    print(f"Email: {form_data.username}")
    print(f"User found: {user is not None}")
    if user:
        print(f"User ID: {user.id}")
        print(f"User Name: {user.name}")
        print(f"Role ID: {user.role_id}")
        print(f"Is Active: {user.is_active}")
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        print(f"Login failed: User not found or invalid password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        print(f"Login failed: User account is deactivated")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Get primary role info - use eager loading to avoid relationship issues
    role_name = None
    permissions = []
    
    if user.role_id:
        role = db.query(models.Role).filter(models.Role.id == user.role_id).first()
        if role:
            role_name = role.name
            permissions = role.permissions if role.permissions else []
            print(f"Role found: {role_name}")
        else:
            # Fallback: role_id exists but role not found
            print(f"Warning: role_id {user.role_id} not found in roles table, using default")
            role_name = "Employee"
            permissions = ["view:assets", "view:assignments", "view:dashboard"]
    else:
        print(f"Warning: User has no role_id assigned")
    
    # Get secondary role info if exists
    has_secondary_role = False
    secondary_role_name = None
    if user.secondary_role_id:
        secondary_role = db.query(models.Role).filter(models.Role.id == user.secondary_role_id).first()
        if secondary_role and secondary_role.id != user.role_id:
            has_secondary_role = True
            secondary_role_name = secondary_role.name
    
    print(f"Login successful for {user.email} as {role_name}")
    print(f"======================\n")
    
    access_token = auth.create_access_token(
        data={
            "sub": user.email, 
            "role": role_name, 
            "permissions": permissions,
            "has_secondary_role": has_secondary_role,
            "secondary_role": secondary_role_name
        },
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "user_id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": role_name,
        "permissions": permissions,
        "has_secondary_role": has_secondary_role,
        "secondary_role": secondary_role_name
    }
