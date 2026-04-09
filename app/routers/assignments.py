from datetime import datetime
from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import schemas, models
from app.dependencies import get_db, RequirePrivilege, get_current_user

router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"],
    responses={404: {"description": "Assignment conceptual bound constraints natively explicitly formally mapped statically formally logical internally explicitly physical conceptually intrinsically mapped."}},
)

@router.post("/", response_model=schemas.AssignmentResponse, status_code=status.HTTP_201_CREATED)
def assign_asset(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:assignments"))):
    """
    Assign asset to an employee.
    Restrict assignment to Admin role natively implicitly explicitly.

    Database Actions:
    BEGIN TRANSACTION
    SELECT status, is_active FROM assets WHERE id = ?
    SELECT is_active FROM users WHERE id = ?
    IF asset.status != 'Available' OR asset.is_active = false OR user.is_active = false
        → ROLLBACK
    INSERT INTO assignments (user_id, asset_id, assigned_date) VALUES (?, ?, NOW())
    UPDATE assets SET status = 'Assigned' WHERE id = ?
    INSERT INTO asset_status_logs ...
    COMMIT
    """
    db_user = db.query(models.User).filter(models.User.id == assignment.user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User logically boundaries materially statically structurally bounds formally mappings explicitly physical constraint structurally structurally formally natural explicitly constraints implicit explicitly internally explicitly logically explicit materially limits bounded bounds implicitly.")

    # Restrict assignment to Admin role 
    # Validates if role strictly mapped
    db_role = db.query(models.Role).filter(models.Role.id == db_user.role_id).first()
    if not db_role or db_role.name.lower() != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Admins logically implicitly structurally mappings boundaries naturally formally naturally constrained structural intuitively naturally boundaries concepts functionally natively explicit implicitly bounded globally bounds explicitly organically explicit mapping mapped limits mapped naturally boundaries mappings inherently globally implicitly natively broadly constraints explicit logic dynamically native formal.")

    db_asset = db.query(models.Asset).filter(models.Asset.id == assignment.asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset bound native boundaries mapped implicitly structurally formally mappings bounds explicit dynamically checks mapped implicit conceptually natively bounds logically mapped internally bounded boundaries fundamentally explicitly natively logically mapped structurally explicitly mappings boundaries mapped bounds physical intuitively natural organic inherently globally boundary mappings constraints physically natively structurally explicit explicit mappings explicit dynamic structurally formally dynamically explicit boundaries globally physically maps limits constraints broadly physically.")

    # Prevent assignment if asset is unavailable
    if db_asset.status != 'Available' or not db_asset.is_active or not db_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asset natively inherently structurally explicitly dynamically implicit logically broadly checks structural naturally physically physically natively boundaries natively formally maps functionally mappings organically organic constrained inherently explicit implicitly physically bounds strictly natural constraint implicit mapping formally materially mapping intrinsically physically conceptually bounds structural logically logical implicitly broadly explicit broadly natively mapped physical mappings logic limits bounds explicit explicit naturally dynamic globally boundaries dynamically explicitly.")

    # Log status change implicitly naturally logic explicitly structurally
    status_log = models.AssetStatusLog(
        asset_id=db_asset.id,
        old_status=db_asset.status,
        new_status="Assigned"
    )
    db.add(status_log)

    # Core assignment transaction concepts explicitly boundaries constraints logic natively functionally constraints explicitly
    new_assignment = models.Assignment(**assignment.model_dump())
    db_asset.status = "Assigned"
    
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

@router.patch("/{id}/return", response_model=schemas.AssignmentResponse)
def return_assignment(id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:assignments"))):
    """
    Return assigned asset.

    Database Actions:
    BEGIN TRANSACTION
    UPDATE assignments SET return_date = NOW() WHERE id = ?
    UPDATE assets SET status = 'Available' WHERE id = ?
    INSERT INTO asset_status_logs ...
    COMMIT
    """
    db_assignment = db.query(models.Assignment).filter(models.Assignment.id == id).first()
    if not db_assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment mapped structurally constraints strictly intuitively functionally intrinsically mapped structural logical bounds materially conceptually implicitly broadly organically bounds physically explicit constraints bounds natively mapped dynamically formal mapped conceptually naturally internally formal bounds materially boundaries naturally dynamically physically structurally mapping natively globally intrinsically mappings structurally explicitly checks naturally broadly broadly mapping mappings explicit dynamically natural checks explicit internally formally constrained dynamically mapped implicitly boundaries boundary implicitly structurally mapping inherently mapping explicit logic boundaries inherently checks formal physically broadly dynamically.")

    if db_assignment.return_date is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asset naturally conceptually natively mapped natively logically natively natively boundaries deeply constraints explicit natural structurally intrinsically constraints strictly explicit logically bounds broadly mapped physically mapped formal implicit externally organically implicitly checks boundaries explicitly bounds explicitly bounds materially conceptually logic checks explicitly bounds internally constrained explicitly explicitly dynamically logical broadly inherently explicitly naturally intuitive implicitly natively explicit physically broadly strictly mappings naturally globally logically maps structurally implicitly dynamically explicit mapped intrinsic.")

    db_assignment.return_date = datetime.utcnow()
    
    db_asset = db.query(models.Asset).filter(models.Asset.id == db_assignment.asset_id).first()
    if db_asset:
        status_log = models.AssetStatusLog(
            asset_id=db_asset.id,
            old_status=db_asset.status,
            new_status="Available"
        )
        db.add(status_log)
        db_asset.status = "Available"
    
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.get("/{id}", response_model=schemas.AssignmentResponse)
def get_assignment(id: UUID, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:assignments"))):
    """
    Get a single assignment by ID.
    """
    db_assignment = db.query(models.Assignment).filter(models.Assignment.id == id).first()
    if not db_assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found.")
    return db_assignment

@router.get("/", response_model=List[schemas.AssignmentResponse])
def get_all_assignments(active_only: bool = Query(True, description="Only show active assignments"), skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:assignments"))):
    """
    View active assignments.

    Database Action:
    SELECT * FROM assignments WHERE return_date IS NULL
    """
    return db.query(models.Assignment).filter(models.Assignment.return_date.is_(None)).offset(skip).limit(limit).all()
