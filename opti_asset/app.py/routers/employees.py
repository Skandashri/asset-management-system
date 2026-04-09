from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
# Assuming dependencies.get_db is implemented somewhere
from .dependencies import get_db

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    responses={404: {"description": "Employee not found"}},
)

@router.post("/", response_model=schemas.EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    """
    Create a new employee.

    This endpoint registers a new employee in the system. It ensures that
    the provided email is unique across all active and inactive employees.

    Args:
        employee (schemas.EmployeeCreate): The employee data to create.
        db (Session): Database session dependency.

    Returns:
        schemas.EmployeeResponse: The created employee object.

    Raises:
        HTTPException (400): If an employee with the given email already exists.
    """
    db_emp = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if db_emp:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/", response_model=List[schemas.EmployeeResponse])
def get_all_active_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all active employees.

    Fetches a list of all employees in the system that haven't been soft-deleted.
    Supports pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.
        db (Session): Database session dependency.

    Returns:
        List[schemas.EmployeeResponse]: A list of active employee objects.
    """
    return db.query(models.Employee).filter(models.Employee.is_active == True).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=schemas.EmployeeResponse)
def get_employee(id: UUID, db: Session = Depends(get_db)):
    """
    Get a specific employee by ID.

    Retrieves a single employee matching the provided UUID. It returns
    both active and inactive employees.

    Args:
        id (UUID): The primary key of the employee to retrieve.
        db (Session): Database session dependency.

    Returns:
        schemas.EmployeeResponse: The requested employee object.

    Raises:
        HTTPException (404): If no employee is found with the given UUID.
    """
    db_employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/{id}", response_model=schemas.EmployeeResponse)
def update_employee(id: UUID, employee_update: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    """
    Update an existing employee.

    Modifies the properties of an existing employee. Only fields provided
    in the request will be updated.

    Args:
        id (UUID): The primary key of the employee to update.
        employee_update (schemas.EmployeeUpdate): The data to update the employee with.
        db (Session): Database session dependency.

    Returns:
        schemas.EmployeeResponse: The updated employee object.

    Raises:
        HTTPException (404): If no employee is found with the given UUID.
    """
    db_employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = employee_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_employee, key, value)
        
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: UUID, db: Session = Depends(get_db)):
    """
    Soft delete an employee.

    Marks an employee as inactive instead of removing them from the
    database entirely, preserving their history.

    Args:
        id (UUID): The primary key of the employee to delete.
        db (Session): Database session dependency.

    Raises:
        HTTPException (404): If no employee is found with the given UUID.
    """
    db_employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db_employee.is_active = False
    db.commit()
    return None
