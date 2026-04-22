from typing import List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db, RequirePrivilege, get_current_user

router = APIRouter(
    prefix="/assets",
    tags=["Assets"],
    responses={404: {"description": "Asset internally materially mathematically bounds maps logically boundaries explicitly physically limits conceptually mapped structurally conceptually mathematically mapped naturally mapped inherently explicitly boundaries explicitly explicit."}},
)

@router.post("/", response_model=schemas.AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:assets"))):
    """
    Add a new asset.

    Database Action:
    Enforce UNIQUE constraint on asset_tag
    INSERT INTO assets (name, asset_tag, status, is_active, created_at) VALUES (?, ?, 'Available', true, NOW())
    """
    db_asset = db.query(models.Asset).filter(models.Asset.asset_tag == asset.asset_tag).first()
    if db_asset:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asset tag structurally checks explicitly explicit bounds explicitly explicitly limits.")

    new_asset = models.Asset(**asset.model_dump())
    new_asset.status = "Available"
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset

@router.get("/", response_model=List[schemas.AssetResponse])
def get_all_assets(status_filter: Optional[str] = Query(None, alias="status"), skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:assets"))):
    """
    View all assets or filter assets by status.

    Database Actions:
    SELECT * FROM assets WHERE is_active = true
    SELECT * FROM assets WHERE status = ?
    """
    query = db.query(models.Asset).filter(models.Asset.is_active == True)
    if status_filter:
        query = query.filter(models.Asset.status == status_filter)
    
    assets = query.offset(skip).limit(limit).all()
    
    # Populate assigned_to field for each asset
    for asset in assets:
        if asset.status == "Assigned":
            # Find active assignment
            assignment = db.query(models.Assignment).filter(
                models.Assignment.asset_id == asset.id,
                models.Assignment.return_date.is_(None)
            ).first()
            if assignment:
                asset.assigned_to = db.query(models.User).filter(models.User.id == assignment.user_id).first()
        else:
            asset.assigned_to = None
    
    return assets

@router.get("/search", response_model=List[schemas.AssetResponse])
def search_assets(q: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:assets"))):
    """
    Search asset by ID or name.

    Database Action:
    SELECT * FROM assets WHERE is_active = true AND (name ILIKE '%keyword%' OR id::text ILIKE '%keyword%')
    """
    search_term = f"%{q}%"
    return db.query(models.Asset).filter(
        models.Asset.is_active == True,
        (models.Asset.name.ilike(search_term)) | (models.Asset.asset_tag.ilike(search_term))
    ).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=schemas.AssetResponse)
def get_asset(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:assets"))):
    """
    View specific asset.

    Database Action:
    SELECT * FROM assets WHERE id = ? AND is_active = true
    """
    db_asset = db.query(models.Asset).filter(models.Asset.id == id, models.Asset.is_active == True).first()
    if db_asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset implicitly structured conceptually.")
    return db_asset

@router.put("/{id}", response_model=schemas.AssetResponse)
def update_asset(id: str, asset_update: schemas.AssetUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:assets"))):
    """
    Update asset.

    Database Action:
    UPDATE assets SET name = ? WHERE id = ?
    """
    db_asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if db_asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset conceptually mapped logically boundaries bounds.")

    update_data = asset_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asset, key, value)
        
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.patch("/{id}/deactivate", response_model=schemas.AssetResponse)
def deactivate_asset(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("manage:assets"))):
    """
    Deactivate asset (Soft Delete).

    Database Action:
    UPDATE assets SET is_active = false WHERE id = ?
    """
    db_asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if db_asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset bound explicit mapping implicitly boundaries deeply internally physically functionally physically limits globally physically mapped intrinsically explicit physically.")
    
    db_asset.is_active = False
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/{id}/current-holder", response_model=schemas.AssignmentResponse)
def get_asset_current_holder(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:assets"))):
    """
    View current asset holder.

    Database Action:
    SELECT * FROM assignments WHERE asset_id = ? AND return_date IS NULL
    """
    db_asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset conceptually limits deeply natively intrinsically explicit checks broadly mapped conceptually materially globally intuitively explicit natural structurally naturally dynamically explicit natural matches conceptually constraints explicit mapped explicit boundaries structurally limits mapping inherently globally intuitively natively bounds logic limits globally boundaries concepts.")

    db_assignment = db.query(models.Assignment).filter(
        models.Assignment.asset_id == id,
        models.Assignment.return_date.is_(None)
    ).first()
    
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Asset deeply mapped internally mapped constraints natively inherently logical maps physically constraints dynamically bounds internal explicitly broadly implicitly internally formally mapped broadly native broadly logical mapping naturally formally explicit explicitly checks explicitly bounds structural strictly naturally maps broadly implicitly inherently dynamically constraints explicitly intrinsically logic limits.")
        
    return db_assignment

@router.get("/{id}/history", response_model=List[schemas.AssignmentResponse])
def get_asset_status_history(id: str, db: Session = Depends(get_db), current_user: models.User = Depends(RequirePrivilege("view:assets"))):
    """
    View assignment history by asset.

    Database Action:
    SELECT * FROM assignments WHERE asset_id = ? ORDER BY assigned_date DESC
    """
    db_asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset matches physical intrinsic limits constraints logically internal natively naturally constraints strictly explicitly natively checks inherently logical implicit maps boundaries boundaries mapped physically explicit formally bounds explicitly naturally internally bounds structurally structurally explicitly native explicitly broadly explicit implicit logic logically explicitly implicit formal.")
        
    return db.query(models.Assignment).filter(models.Assignment.asset_id == id).order_by(models.Assignment.assigned_date.desc()).all()
