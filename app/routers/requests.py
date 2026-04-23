from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app import models, schemas
from app.dependencies import get_db, RequirePrivilege, get_current_user

router = APIRouter(
    prefix="/requests",
    tags=["Requests"],
)

@router.post("/", response_model=schemas.RequestResponse, status_code=status.HTTP_201_CREATED)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_request = models.Request(**request.model_dump(), user_id=current_user.id)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.get("/", response_model=List[schemas.RequestResponse])
def get_all_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:dashboard"))):
    # Use eager loading to ensure user and asset relationships are loaded
    return db.query(models.Request).options(
        joinedload(models.Request.user),
        joinedload(models.Request.asset)
    ).order_by(
        models.Request.requested_at.desc()
    ).offset(skip).limit(limit).all()

@router.get("/my", response_model=List[schemas.RequestResponse])
def get_my_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Use eager loading to ensure user and asset relationships are loaded
    requests = db.query(models.Request).options(
        joinedload(models.Request.user),
        joinedload(models.Request.asset)
    ).filter(
        models.Request.user_id == current_user.id
    ).order_by(
        models.Request.requested_at.desc()
    ).offset(skip).limit(limit).all()
    
    print(f"\n=== Fetching requests for user {current_user.email} ===")
    print(f"Found {len(requests)} requests")
    for req in requests:
        print(f"  Request ID: {req.id}")
        print(f"  Item: {req.item_name}")
        print(f"  Status: {req.status}")
        print(f"  Admin Notes: {req.admin_notes}")
        print(f"  User: {req.user.name if req.user else 'None'}")
    print(f"========================================\n")
    
    return requests

@router.put("/{id}", response_model=schemas.RequestResponse)
def update_request(id: str, request_update: schemas.RequestUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:reports"))):
    db_request = db.query(models.Request).filter(models.Request.id == id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
        
    update_data = request_update.model_dump(exclude_unset=True)
    print(f"\n=== Updating Request {id} ===")
    print(f"Update data: {update_data}")
    
    for key, value in update_data.items():
        setattr(db_request, key, value)
        print(f"  Set {key} = {value}")
        
    db.commit()
    db.refresh(db_request)
    
    print(f"Request updated successfully")
    print(f"  Status: {db_request.status}")
    print(f"  Admin Notes: {db_request.admin_notes}")
    print(f"===========================\n")
    
    return db_request
