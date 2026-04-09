from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class SystemBaseModel(BaseModel):
    """Base model with ORM mode enabled."""
    model_config = ConfigDict(from_attributes=True)

# -----------------
# Role Schemas
# -----------------

class RoleBase(SystemBaseModel):
    name: str = Field(..., description="Unique explicit role name (e.g., 'Admin')")
    permissions: List[str] = Field(default_factory=list, description="List of assigned privileges")

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: UUID = Field(..., description="Primary key of the role")

# -----------------
# User Schemas 
# -----------------

class UserBase(SystemBaseModel):
    name: str = Field(..., description="Full name of the user")
    email: EmailStr = Field(..., description="Unique email address")
    role_id: Optional[UUID] = Field(None, description="Role classification constraint mapping")
    secondary_role_id: Optional[UUID] = Field(None, description="Secondary role for role switching")

class UserCreate(UserBase):
    password: str = Field(..., min_length=4, description="Raw password to be hashed")

class UserUpdate(SystemBaseModel):
    name: Optional[str] = Field(None, description="Full name")
    email: Optional[EmailStr] = Field(None, description="Email constraints")
    role_id: Optional[UUID] = Field(None, description="Change Role mapping limits")
    secondary_role_id: Optional[UUID] = Field(None, description="Set secondary role for switching")
    is_active: Optional[bool] = Field(None, description="Soft deletion logical drops")

class UserRoleUpdate(SystemBaseModel):
    role_id: UUID = Field(..., description="Foreign key linking to Role")

class UserResponse(UserBase):
    id: UUID = Field(..., description="Primary PK bounds")
    is_active: bool = Field(..., description="Soft drop validations")
    created_at: datetime = Field(..., description="Timestamp of setup")
    role: Optional[RoleResponse] = Field(None, description="Mapped relational role object mappings")
    secondary_role: Optional[RoleResponse] = Field(None, description="Secondary role for switching")

# -----------------
# Asset Schemas
# -----------------

class AssetBase(SystemBaseModel):
    asset_tag: str = Field(..., description="Unique intrinsic physical tags binding queries")
    name: str = Field(..., description="Asset mapping names explicitly categorizing strings")

class AssetCreate(AssetBase):
    pass

class AssetUpdate(SystemBaseModel):
    asset_tag: Optional[str] = Field(None, description="Physical unique query tagging limits")
    name: Optional[str] = Field(None, description="Renamed explicit tags")
    status: Optional[str] = Field(None, description="Must match explicit values (Available, Assigned)")
    is_active: Optional[bool] = Field(None, description="Boolean constraint omitting row values soft drops logically")

class AssetStatusLogResponse(SystemBaseModel):
    id: UUID
    old_status: Optional[str]
    new_status: str
    changed_at: datetime

class AssetResponse(AssetBase):
    id: UUID = Field(..., description="UUID mappings statically bound uniquely natively logically")
    status: str = Field(..., description="Intrinsic assigned available enumerations constraints")
    is_active: bool = Field(..., description="Soft drops bool evaluations inherently statically dropped")
    created_at: datetime = Field(..., description="Initial stamps values implicitly broadly mapped")
    status_logs: Optional[List[AssetStatusLogResponse]] = Field(None, description="Mapping explicit inherently lists logically intrinsic")

# -----------------
# Assignment Schemas
# -----------------

class AssignmentBase(SystemBaseModel):
    user_id: UUID = Field(..., description="Foreign key mapping explicit bounds")
    asset_id: UUID = Field(..., description="Mapping logical broadly explicitly logically implies constraints")

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    id: UUID = Field(..., description="Intrinsic queries statically intrinsic.")
    assigned_date: datetime = Field(..., description="Stamps internally natural.")
    return_date: Optional[datetime] = Field(None, description="Maps constraints internally physically bounds.")
    user: Optional[UserResponse] = Field(None, description="Mapped explicitly matches implicitly.")
    asset: Optional[AssetResponse] = Field(None, description="Matches mapped structurally logically deeply.")

# -----------------
# Dashboard Schemas
# -----------------

class DashboardStats(BaseModel):
    total_assets: int
    active_assignments: int
    available_inventory: int
    total_employees: int
    pending_reports: int  # New field for reports

class AssetReportBase(SystemBaseModel):
    asset_id: UUID = Field(..., description="Asset being reported")
    report_type: str = Field(..., description="Type: Damaged, Lost, Stolen, Maintenance Required")
    description: str = Field(..., description="Detailed description of the issue")
    severity: str = Field(default="Medium", description="Low, Medium, High, Critical")

class AssetReportCreate(AssetReportBase):
    pass

class AssetReportUpdate(SystemBaseModel):
    status: Optional[str] = Field(None, description="Pending, Under Review, Resolved, Rejected")
    admin_notes: Optional[str] = Field(None, description="Admin resolution notes")

class AssetReportResponse(AssetReportBase):
    id: UUID = Field(..., description="Report ID")
    reported_by_id: UUID = Field(..., description="User who reported")
    status: str = Field(..., description="Current status")
    created_at: datetime = Field(..., description="When reported")
    resolved_at: Optional[datetime] = Field(None, description="When resolved")
    admin_notes: Optional[str] = Field(None, description="Admin notes")
    asset: Optional[AssetResponse] = Field(None, description="Related asset details")
    reported_by: Optional[UserResponse] = Field(None, description="User who reported")

class DashboardResponse(SystemBaseModel):
    total_assets: int = Field(..., description="Static counts naturally.")
    total_users: int = Field(..., description="Counts naturally.")
    available_assets: int = Field(..., description="Constraints counts mathematically bounds conceptually.")
    assigned_assets: int = Field(..., description="Bounds explicitly mapping queries.")
    pending_reports: int = Field(default=0, description="Number of pending asset reports")

# Rebuild models
UserResponse.model_rebuild()
AssetResponse.model_rebuild()
AssignmentResponse.model_rebuild()

# -----------------
# Auth Schemas
# -----------------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
