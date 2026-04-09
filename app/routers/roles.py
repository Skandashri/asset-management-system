from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db, RequirePrivilege, get_current_user

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    responses={404: {"description": "Role not found"}},
)

@router.post("/", response_model=schemas.RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:roles"))):
    """
    Create a new role.

    Registers a new Role defined by the name (e.g., 'Admin', 'Employee'). 
    Validates name uniqueness globally.

    Args:
        role (schemas.RoleCreate): The role name string.
        db (Session): Database session dependency.

    Returns:
        schemas.RoleResponse: Generated Role object with UUID bounds.

    Raises:
        HTTPException (400): If the role name is already registered.
    """
    db_role = db.query(models.Role).filter(models.Role.name == role.name).first()
    if db_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role explicitly exists mapping.")
        
    new_role = models.Role(**role.model_dump())
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@router.get("/", response_model=List[schemas.RoleResponse])
def get_all_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:roles"))):
    """
    Retrieve all registered semantic roles natively internally functionally explicitly mapped boundaries logically mapped implicitly concepts.
    """
    return db.query(models.Role).offset(skip).limit(limit).all()
