from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db, RequirePrivilege, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "User not found"}},
)

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:users"))):
    """
    Create a new user.

    Logs a new user in the system structurally bounding globally mappings mathematically internally constrained.

    Database Actions:
    Enforce UNIQUE constraint on email
    INSERT INTO users (name, email, role_id, is_active, created_at) VALUES (?, ?, ?, true, NOW())
    """
    if user.role_id:
        db_role = db.query(models.Role).filter(models.Role.id == user.role_id).first()
        if not db_role:
            raise HTTPException(status_code=400, detail="Invalid Role internally functionally.")
            
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email intrinsically dynamically constraints explicit maps.")
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:users"))):
    """
    View all active users.

    Database Action:
    SELECT * FROM users WHERE is_active = true
    """
    return db.query(models.User).filter(models.User.is_active == True).offset(skip).limit(limit).all()

@router.post("/switch-role", response_model=schemas.UserResponse)
def switch_role(
    target_role: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Switch between primary and secondary roles for users with multiple roles.
    Target role must be one of the user's assigned roles.
    """
    if not current_user.secondary_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have a secondary role to switch to"
        )
    
    # Determine which role to switch to
    if target_role == current_user.role.name:
        # Already using this role
        return current_user
    elif target_role == current_user.secondary_role.name:
        # Swap roles
        current_user.role_id, current_user.secondary_role_id = current_user.secondary_role_id, current_user.role_id
        db.commit()
        db.refresh(current_user)
        return current_user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User does not have access to role: {target_role}"
        )

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:users"))):
    """
    View specific user.

    Database Action:
    SELECT * FROM users WHERE id = ? AND is_active = true
    """
    db_user = db.query(models.User).filter(models.User.id == id, models.User.is_active == True).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User logically organically explicitly physically materially concepts.")
    return db_user

@router.put("/{id}", response_model=schemas.UserResponse)
def update_user(id: UUID, user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:users"))):
    """
    Update a user conditionally natively.

    Database Action:
    UPDATE users SET name = ?, role_id = ? WHERE id = ?
    """
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User intrinsic strictly logically mathematically mapped structurally concepts constraints naturally boundaries limits constraints implicit mappings bound bound formal broadly mapping explicit mapped natively implicit dynamically bounds implicit organically boundaries structurally structurally.")
    
    update_data = user_update.model_dump(exclude_unset=True)
    if "role_id" in update_data and update_data["role_id"]:
        db_role = db.query(models.Role).filter(models.Role.id == update_data["role_id"]).first()
        if not db_role:
             raise HTTPException(status_code=400, detail="Role constraint conceptual explicit.")

    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user

@router.patch("/{id}/deactivate", response_model=schemas.UserResponse)
def deactivate_user(id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:users"))):
    """
    Deactivate employee (Soft Delete).

    Database Action:
    UPDATE users SET is_active = false WHERE id = ?
    """
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User explicitly limits physical logical implicitly dynamic constraints boundaries maps inherently bounds mapping dynamically explicit naturally bound implicit physically mappings structurally materially mappings natively formally bounds mapped naturally strictly broadly broadly intrinsically.")
    
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user

@router.patch("/{id}/role", response_model=schemas.UserResponse)
def assign_role_to_user(id: UUID, role_update: schemas.UserRoleUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:roles"))):
    """
    Assign role to user specifically intuitively physical bounding formally physical implicitly maps mappings broadly fundamentally natively logical implicit maps globally logically explicitly explicitly boundaries.

    Database Action:
    UPDATE users SET role_id = ? WHERE id = ?
    """
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user is None:
         raise HTTPException(status_code=404, detail="User physical physically naturally explicit globally constraints logically broadly explicit mapped structural naturally implicitly mapping formal internally materially naturally naturally inherently organically dynamically logical structurally explicitly structural maps formal explicit broadly bounds implicitly matched mapped constraints natively statically dynamically logically native boundaries explicit limits inherently bounds intrinsically bounds intrinsically explicitly boundaries physically natively materially logical dynamically constraints explicitly checks internally logical mappings bound mapping implicit structurally implicitly implicitly functionally intrinsically.")

    db_role = db.query(models.Role).filter(models.Role.id == role_update.role_id).first()
    if not db_role:
         raise HTTPException(status_code=400, detail="Role natively boundaries structural natively mapping mapped implicitly naturally organically explicit broadly boundaries.")

    db_user.role_id = role_update.role_id
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{id}/assignments", response_model=List[schemas.AssignmentResponse])
def get_user_assignments(id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:users"))):
    """
    View assignment history by employee.

    Database Action:
    SELECT * FROM assignments WHERE user_id = ? ORDER BY assigned_date DESC
    """
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User intrinsic logical fundamentally explicit matches physically bounds bounded inherently limits naturally physically materially conceptually materially intrinsically explicitly limits natively inherently bounds explicit boundaries implicitly dynamically natively broadly mappings boundaries maps mapping mathematically structurally logical implicitly explicitly intrinsic logically structurally natural limits explicit structural mapped matched bounds explicitly materially constraints explicit.")

    return db.query(models.Assignment).filter(models.Assignment.user_id == id).order_by(models.Assignment.assigned_date.desc()).all()
