from uuid import UUID
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
# Assuming dependencies.get_db is implemented somewhere
from .dependencies import get_db

router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"],
    responses={404: {"description": "Assignment not found"}},
)

@router.post("/", response_model=schemas.AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    """
    Create a new assignment.

    Assigns an asset to an employee. It validates whether both the employee
    and the asset exist. It enforces the business rule that prevents an
    assignment if the asset is currently unavailable. Upon successful
    assignment, the asset's availability is set to False.

    Args:
        assignment (schemas.AssignmentCreate): The assignment data containing employee_id and asset_id.
        db (Session): Database session dependency.

    Returns:
        schemas.AssignmentResponse: The created assignment object.

    Raises:
        HTTPException (404): If the employee or asset is not found.
        HTTPException (400): If the asset is currently unavailable.
    """
    db_employee = db.query(models.Employee).filter(models.Employee.id == assignment.employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    db_asset = db.query(models.Asset).filter(models.Asset.id == assignment.asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    if not db_asset.is_available:
        raise HTTPException(status_code=400, detail="Asset is currently unavailable for assignment")
        
    # Set asset to unavailable
    db_asset.is_available = False
    
    db_assignment = models.Assignment(**assignment.model_dump())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.post("/{id}/return", response_model=schemas.AssignmentResponse)
def return_assignment(id: UUID, db: Session = Depends(get_db)):
    """
    Return an assigned asset.

    Marks an active assignment as returned by setting the returned_at timestamp
    to the current time. It also updates the associated asset's availability
    back to True, allowing it to be assigned again.

    Args:
        id (UUID): The primary key of the assignment to return.
        db (Session): Database session dependency.

    Returns:
        schemas.AssignmentResponse: The updated assignment object with returned_at populated.

    Raises:
        HTTPException (404): If the assignment is not found.
        HTTPException (400): If the assignment has already been returned.
    """
    db_assignment = db.query(models.Assignment).filter(models.Assignment.id == id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
        
    if db_assignment.returned_at is not None:
        raise HTTPException(status_code=400, detail="Assignment has already been returned")
        
    db_assignment.returned_at = datetime.utcnow()
    
    db_asset = db.query(models.Asset).filter(models.Asset.id == db_assignment.asset_id).first()
    if db_asset:
        db_asset.is_available = True
        
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.get("/", response_model=List[schemas.AssignmentResponse])
def get_all_assignments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all assignments.

    Fetches a list of all asset assignments (both active and returned)
    in the system. Supports pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.
        db (Session): Database session dependency.

    Returns:
        List[schemas.AssignmentResponse]: A list of assignment objects.
    """
    return db.query(models.Assignment).offset(skip).limit(limit).all()

@router.get("/history/{employee_id}", response_model=List[schemas.AssignmentResponse])
def get_employee_assignment_history(employee_id: UUID, db: Session = Depends(get_db)):
    """
    Get assignment history for a specific employee.

    Retrieves all past and present asset assignments for a given employee.

    Args:
        employee_id (UUID): The primary key of the employee.
        db (Session): Database session dependency.

    Returns:
        List[schemas.AssignmentResponse]: A list of assignment objects linked to the employee.

    Raises:
        HTTPException (404): If the employee is not found.
    """
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    return db.query(models.Assignment).filter(models.Assignment.employee_id == employee_id).all()
