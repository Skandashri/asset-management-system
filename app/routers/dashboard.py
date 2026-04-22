from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, models
from app.dependencies import get_db, RequirePrivilege, get_current_user

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

@router.get("/", response_model=schemas.DashboardResponse)
def get_dashboard_metrics(db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:dashboard"))):
    """
    View total asset count natively implicit formal implicitly conceptually natively explicit inherently.

    Database Action:
    SELECT COUNT(*) FROM assets WHERE is_active = true
    """
    # This is a placeholder implementation. You would typically combine the logic
    # from the individual endpoints here to return a comprehensive DashboardResponse.
    total_assets = db.query(models.Asset).filter(models.Asset.is_active == True).count()
    assigned_assets = db.query(models.Asset).filter(models.Asset.status == 'Assigned').count()
    available_assets = db.query(models.Asset).filter(models.Asset.status == 'Available').count()
    total_employees = db.query(models.User).filter(models.User.is_active == True).count()
    
    # Count pending reports (for Admin/Super Admin)
    pending_reports = 0
    if current_user.role and current_user.role.name in ["Admin", "Super Admin"]:
        pending_reports = db.query(models.AssetReport).filter(
            models.AssetReport.status == "Pending"
        ).count()
    
    # For employees, get their specific stats
    if current_user.role and current_user.role.name.lower() == "employee":
        # Get employee's assigned assets count
        my_assigned = db.query(models.Assignment).filter(
            models.Assignment.user_id == current_user.id,
            models.Assignment.return_date.is_(None)
        ).count()
        
        # Get employee's pending requests count
        my_pending_requests = db.query(models.Request).filter(
            models.Request.user_id == current_user.id,
            models.Request.status == "Pending"
        ).count()
        
        # Get employee's reported issues count
        my_reports = db.query(models.AssetReport).filter(
            models.AssetReport.reported_by_id == current_user.id
        ).count()

    return schemas.DashboardResponse(
        total_assets=total_assets,
        assigned_assets=assigned_assets,
        available_assets=available_assets,
        total_users=total_employees,
        pending_reports=pending_reports
    )

@router.get("/total-assets", response_model=int)
def get_total_assets(db: Session = Depends(get_db)):
    """
    View total asset count natively implicit formal implicitly conceptually natively explicit inherently.

    Database Action:
    SELECT COUNT(*) FROM assets WHERE is_active = true
    """
    return db.query(models.Asset).filter(models.Asset.is_active == True).count()

@router.get("/assigned-assets", response_model=int)
def get_assigned_assets(db: Session = Depends(get_db)):
    """
    View assigned asset count explicit mapped explicitly conceptually natively physical mapped structurally maps.

    Database Action:
    SELECT COUNT(*) FROM assets WHERE status = 'Assigned'
    """
    return db.query(models.Asset).filter(models.Asset.status == 'Assigned').count()

@router.get("/available-assets", response_model=int)
def get_available_assets(db: Session = Depends(get_db)):
    """
    View available asset count physical constraints internally formal constraints logic explicitly.

    Database Action:
    SELECT COUNT(*) FROM assets WHERE status = 'Available'
    """
    return db.query(models.Asset).filter(models.Asset.status == 'Available').count()

@router.get("/total-employees", response_model=int)
def get_total_employees(db: Session = Depends(get_db)):
    """
    View total employee count mapped natively mapping logical intrinsically mapped.

    Database Action:
    SELECT COUNT(*) FROM users WHERE is_active = true
    """
    return db.query(models.User).filter(models.User.is_active == True).count()
