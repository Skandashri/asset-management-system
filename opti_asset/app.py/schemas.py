from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# -----------------
# Base Configurations
# -----------------

class SystemBaseModel(BaseModel):
    """Base model with ORM mode enabled."""
    model_config = ConfigDict(from_attributes=True)

# -----------------
# Employee Schemas
# -----------------

class EmployeeBase(SystemBaseModel):
    """Base schema for Employee properties."""
    name: str = Field(..., description="Full name of the employee")
    email: EmailStr = Field(..., description="Unique email address")
    department: Optional[str] = Field(None, description="Department the employee belongs to")

class EmployeeCreate(EmployeeBase):
    """Schema for creating a new Employee."""
    pass

class EmployeeUpdate(SystemBaseModel):
    """Schema for updating an existing Employee."""
    name: Optional[str] = Field(None, description="Full name of the employee")
    email: Optional[EmailStr] = Field(None, description="Unique email address")
    department: Optional[str] = Field(None, description="Department the employee belongs to")
    is_active: Optional[bool] = Field(None, description="Flag for soft deletion")

class EmployeeResponse(EmployeeBase):
    """Schema for Employee response data."""
    id: UUID = Field(..., description="Primary key for the employee")
    is_active: bool = Field(..., description="Flag for soft deletion")
    created_at: datetime = Field(..., description="Timestamp of creation")

# -----------------
# Asset Schemas
# -----------------

class AssetBase(SystemBaseModel):
    """Base schema for Asset properties."""
    asset_tag: str = Field(..., description="Unique tag for the asset")
    name: Optional[str] = Field(None, description="Name of the asset")
    description: Optional[str] = Field(None, description="Detailed description of the asset")

class AssetCreate(AssetBase):
    """Schema for creating a new Asset."""
    pass

class AssetUpdate(SystemBaseModel):
    """Schema for updating an existing Asset."""
    asset_tag: Optional[str] = Field(None, description="Unique tag for the asset")
    name: Optional[str] = Field(None, description="Name of the asset")
    description: Optional[str] = Field(None, description="Detailed description of the asset")
    is_available: Optional[bool] = Field(None, description="Flag indicating if the asset can be assigned")
    is_active: Optional[bool] = Field(None, description="Flag for soft deletion")

class AssetResponse(AssetBase):
    """Schema for Asset response data."""
    id: UUID = Field(..., description="Primary key for the asset")
    is_available: bool = Field(..., description="Flag indicating if the asset can be assigned")
    is_active: bool = Field(..., description="Flag for soft deletion")
    created_at: datetime = Field(..., description="Timestamp of creation")

# -----------------
# Assignment Schemas
# -----------------

class AssignmentBase(SystemBaseModel):
    """Base schema for Assignment properties."""
    employee_id: UUID = Field(..., description="Foreign key linking to the assigned employee")
    asset_id: UUID = Field(..., description="Foreign key linking to the assigned asset")

class AssignmentCreate(AssignmentBase):
    """Schema for creating a new Assignment."""
    pass

class AssignmentUpdate(SystemBaseModel):
    """Schema for updating an Assignment (e.g., setting returned_at)."""
    returned_at: datetime = Field(..., description="Timestamp when the asset was returned")

class AssignmentResponse(AssignmentBase):
    """Schema for Assignment response data."""
    id: UUID = Field(..., description="Primary key for the assignment")
    assigned_at: datetime = Field(..., description="Timestamp when the asset was assigned")
    returned_at: Optional[datetime] = Field(None, description="Timestamp when the asset was returned")
    
    employee: Optional[EmployeeResponse] = Field(None, description="Assigned employee details")
    asset: Optional[AssetResponse] = Field(None, description="Assigned asset details")

# Rebuild models to resolve forward references
AssignmentResponse.model_rebuild()
