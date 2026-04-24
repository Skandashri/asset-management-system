from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db, RequirePrivilege, get_current_user

router = APIRouter(
    prefix="/reports",
    tags=["Asset Reports"],
)

@router.post("/", response_model=schemas.AssetReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(
    report: schemas.AssetReportCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new asset report (damaged, lost, stolen, etc.)
    Available to all authenticated users.
    """
    # Verify asset exists
    db_asset = db.query(models.Asset).filter(models.Asset.id == report.asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    
    # Create the report
    new_report = models.AssetReport(
        **report.model_dump(),
        reported_by_id=current_user.id
    )
    
    db.add(new_report)
    
    # Update asset status to indicate it has a reported issue
    if db_asset.status != 'Issue Reported':
        old_status = db_asset.status
        db_asset.status = 'Issue Reported'
        # Log the status change
        status_log = models.AssetStatusLog(
            asset_id=db_asset.id,
            old_status=old_status,
            new_status="Issue Reported"
        )
        db.add(status_log)
    
    db.commit()
    db.refresh(new_report)
    
    return new_report

@router.get("/my-reports", response_model=List[schemas.AssetReportResponse])
def get_my_reports(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get all reports submitted by the current user.
    """
    reports = db.query(models.AssetReport).filter(
        models.AssetReport.reported_by_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return reports

@router.get("/", response_model=List[schemas.AssetReportResponse])
def get_all_reports(
    status_filter: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(RequirePrivilege("view:reports"))
):
    """
    Get all asset reports (Admin/Super Admin only).
    Can filter by status: Pending, Under Review, Resolved, Rejected
    """
    query = db.query(models.AssetReport)
    
    if status_filter:
        query = query.filter(models.AssetReport.status == status_filter)
    
    reports = query.offset(skip).limit(limit).all()
    return reports

@router.get("/{id}", response_model=schemas.AssetReportResponse)
def get_report(
    id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(RequirePrivilege("view:reports"))
):
    """
    Get specific report details (Admin/Super Admin only).
    """
    report = db.query(models.AssetReport).filter(models.AssetReport.id == id).first()
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    
    return report

@router.put("/{id}", response_model=schemas.AssetReportResponse)
def update_report(
    id: str,
    report_update: schemas.AssetReportUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(RequirePrivilege("manage:reports"))
):
    """
    Update report status and add admin notes (Admin/Super Admin only).
    """
    db_report = db.query(models.AssetReport).filter(models.AssetReport.id == id).first()
    if not db_report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
    
    update_data = report_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_report, key, value)
    
    # If status is being updated to Resolved, set resolved_at
    if 'status' in update_data and update_data['status'] == 'Resolved':
        from datetime import datetime
        db_report.resolved_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_report)
    return db_report
