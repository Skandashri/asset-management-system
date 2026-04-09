from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
# Assuming dependencies.get_db is implemented somewhere
from .dependencies import get_db

router = APIRouter(
    prefix="/assets",
    tags=["Assets"],
    responses={404: {"description": "Asset not found"}},
)

@router.post("/", response_model=schemas.AssetResponse, status_code=status.HTTP_201_CREATED)
def create_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    """
    Create a new asset.

    Registers a new physical or digital asset. It ensures that
    the provided asset tag is unique.

    Args:
        asset (schemas.AssetCreate): The asset data to create.
        db (Session): Database session dependency.

    Returns:
        schemas.AssetResponse: The created asset object.

    Raises:
        HTTPException (400): If an asset with the given tag already exists.
    """
    db_asset = db.query(models.Asset).filter(models.Asset.asset_tag == asset.asset_tag).first()
    if db_asset:
        raise HTTPException(status_code=400, detail="Asset tag already registered")
    
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.get("/", response_model=List[schemas.AssetResponse])
def get_all_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all active assets.

    Fetches a list of all assets that haven't been soft-deleted.
    Supports pagination.

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.
        db (Session): Database session dependency.

    Returns:
        List[schemas.AssetResponse]: A list of active asset objects.
    """
    return db.query(models.Asset).filter(models.Asset.is_active == True).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=schemas.AssetResponse)
def get_asset(id: UUID, db: Session = Depends(get_db)):
    """
    Get a specific asset by ID.

    Retrieves a single asset matching the provided UUID. Returns
    both active and inactive assets.

    Args:
        id (UUID): The primary key of the asset to retrieve.
        db (Session): Database session dependency.

    Returns:
        schemas.AssetResponse: The requested asset object.

    Raises:
        HTTPException (404): If no asset is found with the given UUID.
    """
    db_asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset

@router.put("/{id}", response_model=schemas.AssetResponse)
def update_asset(id: UUID, asset_update: schemas.AssetUpdate, db: Session = Depends(get_db)):
    """
    Update an existing asset.

    Modifies the properties of an existing asset. Only fields provided
    in the request will be updated.

    Args:
        id (UUID): The primary key of the asset to update.
        asset_update (schemas.AssetUpdate): The data to update the asset with.
        db (Session): Database session dependency.

    Returns:
        schemas.AssetResponse: The updated asset object.

    Raises:
        HTTPException (404): If no asset is found with the given UUID.
    """
    db_asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    update_data = asset_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asset, key, value)
        
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(id: UUID, db: Session = Depends(get_db)):
    """
    Soft delete an asset.

    Marks an asset as inactive instead of removing it from the
    database entirely.

    Args:
        id (UUID): The primary key of the asset to delete.
        db (Session): Database session dependency.

    Raises:
        HTTPException (404): If no asset is found with the given UUID.
    """
    db_asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    db_asset.is_active = False
    db.commit()
    return None
