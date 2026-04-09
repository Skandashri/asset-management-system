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
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Get primary role info
    role_name = user.role.name if user.role else None
    permissions = user.role.permissions if user.role and user.role.permissions else []
    
    # Get secondary role info if exists
    has_secondary_role = False
    secondary_role_name = None
    if user.secondary_role and user.secondary_role.id != user.role_id:
        has_secondary_role = True
        secondary_role_name = user.secondary_role.name
    
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
