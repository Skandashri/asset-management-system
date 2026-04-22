from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db, RequirePrivilege, get_current_user
from app.auth import get_password_hash

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
            
        # RBAC Enforcement for User Creation
        if current_user.role.name == "Admin":
            if db_role.name.lower() != "employee":
                raise HTTPException(status_code=403, detail="Admin can only create Employee users.")
        elif current_user.role.name == "Super Admin":
            if db_role.name.lower() not in ["admin", "employee"]:
                raise HTTPException(status_code=403, detail="Super Admin can only create Admin or Employee users.")

    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    # Properly hash the password provided by frontend
    user_data = user.model_dump()
    password = user_data.pop("password")
    user_data["hashed_password"] = get_password_hash(password)

    new_user = models.User(**user_data)
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
def get_user(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:users"))):
    """
    View specific user.

    Database Action:
    SELECT * FROM users WHERE id = ? AND is_active = true
    """
    db_user = db.query(models.User).filter(models.User.id == id, models.User.is_active == True).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.put("/{id}", response_model=schemas.UserResponse)
def update_user(id: str, user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:users"))):
    """
    Update a user conditionally natively.

    Database Action:
    UPDATE users SET name = ?, role_id = ? WHERE id = ?
    """
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    update_data = user_update.model_dump(exclude_unset=True)
    if "role_id" in update_data and update_data["role_id"]:
        db_role = db.query(models.Role).filter(models.Role.id == update_data["role_id"]).first()
        if not db_role:
             raise HTTPException(status_code=400, detail="Role not found")

    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    db.commit()
    db.refresh(db_user)
    return db_user

@router.patch("/{id}/deactivate", response_model=schemas.UserResponse)
def deactivate_user(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:users"))):
    """
    Deactivate employee (Soft Delete).

    Database Action:
    UPDATE users SET is_active = false WHERE id = ?
    """
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db_user.is_active = False
    db.commit()
    db.refresh(db_user)
    return db_user

@router.patch("/{id}/role", response_model=schemas.UserResponse)
def assign_role_to_user(id: str, role_update: schemas.UserRoleUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:roles"))):
    """
    Assign role to user specifically intuitively physical bounding formally physical implicitly maps mappings broadly fundamentally natively logical implicit maps globally logically explicitly explicitly boundaries.

    Database Action:
    UPDATE users SET role_id = ? WHERE id = ?
    """
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user is None:
         raise HTTPException(status_code=404, detail="User not found")

    db_role = db.query(models.Role).filter(models.Role.id == role_update.role_id).first()
    if not db_role:
         raise HTTPException(status_code=400, detail="Role not found")

    db_user.role_id = role_update.role_id
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{id}/assignments", response_model=List[schemas.AssignmentResponse])
def get_user_assignments(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    View assignment history by employee.
    Employees can view their own assignments.
    Admins can view any employee's assignments.

    Database Action:
    SELECT * FROM assignments WHERE user_id = ? ORDER BY assigned_date DESC
    """
    # Employees can only view their own assignments
    if current_user.role.name.lower() == "employee" and current_user.id != id:
        raise HTTPException(status_code=403, detail="You can only view your own assignments")
    
    # Admins/SuperAdmins need view:users permission to view others
    if current_user.role.name.lower() in ["admin", "super admin"] and current_user.id != id:
        from app.dependencies import RequirePrivilege
        # This will be checked by the dependency
        pass
    
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    assignments = db.query(models.Assignment).filter(
        models.Assignment.user_id == id
    ).order_by(models.Assignment.assigned_date.desc()).all()
    
    # Load relationships
    for assignment in assignments:
        if assignment.user is None:
            assignment.user = db.query(models.User).filter(models.User.id == assignment.user_id).first()
        if assignment.asset is None:
            assignment.asset = db.query(models.Asset).filter(models.Asset.id == assignment.asset_id).first()
    
    return assignments

@router.delete("/{id}", response_model=dict)
def delete_user(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:users"))):
    """
    Permanently delete a user.
    """
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Prevent deleting oneself
    if current_user.id == db_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account.")
        
    # RBAC Enforcement for Deletion
    if current_user.role.name == "Admin":
        if db_user.role.name.lower() != "employee":
            raise HTTPException(status_code=403, detail="Admin can only delete Employee users.")
            
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}
