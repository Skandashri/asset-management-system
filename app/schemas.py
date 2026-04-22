from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, date

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
    id: str = Field(..., description="Primary key of the role")

# -----------------
# User Schemas 
# -----------------

class UserBase(SystemBaseModel):
    name: str = Field(..., description="Full name of the user")
    email: EmailStr = Field(..., description="Unique email address")
    role_id: Optional[str] = Field(None, description="Role classification constraint mapping")
    secondary_role_id: Optional[str] = Field(None, description="Secondary role for role switching")
    department: Optional[str] = Field(None, description="Department name")
    contact: Optional[str] = Field(None, description="Contact details")

class UserCreate(UserBase):
    password: str = Field(..., min_length=4, description="Raw password to be hashed")

class UserUpdate(SystemBaseModel):
    name: Optional[str] = Field(None, description="Full name")
    email: Optional[EmailStr] = Field(None, description="Email constraints")
    role_id: Optional[str] = Field(None, description="Change Role mapping limits")
    secondary_role_id: Optional[str] = Field(None, description="Set secondary role for switching")
    department: Optional[str] = Field(None, description="Department name")
    contact: Optional[str] = Field(None, description="Contact details")
    is_active: Optional[bool] = Field(None, description="Soft deletion logical drops")

class UserRoleUpdate(SystemBaseModel):
    role_id: str = Field(..., description="Foreign key linking to Role")

class UserResponse(UserBase):
    id: str = Field(..., description="Primary PK bounds")
    is_active: bool = Field(..., description="Soft drop validations")
    created_at: datetime = Field(..., description="Timestamp of setup")
    role: Optional[RoleResponse] = Field(None, description="Mapped relational role object mappings")
    secondary_role: Optional[RoleResponse] = Field(None, description="Secondary role for switching")

# -----------------
# Asset Schemas
# -----------------

class AssetCategoryBase(SystemBaseModel):
    name: str = Field(..., description="Unique category name")

class AssetCategoryCreate(AssetCategoryBase):
    pass

class AssetCategoryResponse(AssetCategoryBase):
    id: str
    total_quantity: int
    available_quantity: int

class AssetBase(SystemBaseModel):
    asset_tag: str = Field(..., description="Unique intrinsic physical tags binding queries")
    name: str = Field(..., description="Asset mapping names explicitly categorizing strings")
    category_id: Optional[str] = Field(None, description="Asset category mapped")
    purchase_date: Optional[date] = Field(None, description="Purchase date")
    cost: Optional[float] = Field(None, description="Asset cost")
    image_url: Optional[str] = Field(None, description="Image URL")
    document_url: Optional[str] = Field(None, description="Document URL")
    vendor: Optional[str] = Field(None, description="Vendor or supplier")
    location: Optional[str] = Field(None, description="Physical location")

class AssetCreate(AssetBase):
    pass

class AssetUpdate(SystemBaseModel):
    asset_tag: Optional[str] = Field(None, description="Physical unique query tagging limits")
    name: Optional[str] = Field(None, description="Renamed explicit tags")
    category_id: Optional[str] = Field(None, description="Asset category mapped")
    purchase_date: Optional[date] = Field(None, description="Purchase date")
    cost: Optional[float] = Field(None, description="Asset cost")
    image_url: Optional[str] = Field(None, description="Image URL")
    document_url: Optional[str] = Field(None, description="Document URL")
    vendor: Optional[str] = Field(None, description="Vendor or supplier")
    location: Optional[str] = Field(None, description="Asset location")
    status: Optional[str] = Field(None, description="Must match explicit values (Available, Assigned)")
    is_active: Optional[bool] = Field(None, description="Boolean constraint omitting row values soft drops logically")

class AssetStatusLogResponse(SystemBaseModel):
    id: str
    old_status: Optional[str]
    new_status: str
    changed_at: datetime

class AssetResponse(AssetBase):
    id: str = Field(..., description="Asset ID")
    status: str = Field(..., description="Intrinsic assigned available enumerations constraints")
    is_active: bool = Field(..., description="Soft drops bool evaluations inherently statically dropped")
    created_at: datetime = Field(..., description="Initial stamps values implicitly broadly mapped")
    category_rel: Optional[AssetCategoryResponse] = Field(None, description="Linked category data")
    status_logs: Optional[List[AssetStatusLogResponse]] = Field(None, description="Mapping explicit inherently lists logically intrinsic")
    assigned_to: Optional[UserResponse] = Field(None, description="User currently assigned to this asset")

# -----------------
# Assignment Schemas
# -----------------

class AssignmentBase(SystemBaseModel):
    user_id: str = Field(..., description="Foreign key mapping explicit bounds")
    asset_id: str = Field(..., description="Mapping logical broadly explicitly logically implies constraints")

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    id: str = Field(..., description="Intrinsic queries statically intrinsic.")
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
    asset_id: str = Field(..., description="Asset being reported")
    report_type: str = Field(..., description="Type: Damaged, Lost, Stolen, Maintenance Required")
    description: str = Field(..., description="Detailed description of the issue")
    severity: str = Field(default="Medium", description="Low, Medium, High, Critical")

class AssetReportCreate(AssetReportBase):
    pass

class AssetReportUpdate(SystemBaseModel):
    status: Optional[str] = Field(None, description="Pending, Under Review, Resolved, Rejected")
    admin_notes: Optional[str] = Field(None, description="Admin resolution notes")

class AssetReportResponse(AssetReportBase):
    id: str = Field(..., description="Report ID")
    reported_by_id: str = Field(..., description="User who reported")
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
    total_valuation: Optional[float] = Field(default=0.0, description="Total financial valuation of all active assets")

# -----------------
# Request Schemas
# -----------------

class RequestBase(SystemBaseModel):
    item_name: str = Field(..., description="Name of the requested item")
    item_type: str = Field(..., description="Type: Equipment, Accessory, Software, Other")
    notes: Optional[str] = Field(None, description="Detailed description of the request")

class RequestCreate(RequestBase):
    pass

class RequestUpdate(SystemBaseModel):
    status: Optional[str] = Field(None, description="Pending, Approved, Rejected")
    admin_notes: Optional[str] = Field(None, description="Mandatory when rejected")
    asset_id: Optional[str] = Field(None, description="Asset to assign upon approval")

class RequestResponse(RequestBase):
    id: str = Field(..., description="Request ID")
    user_id: str = Field(..., description="User who requested")
    asset_id: Optional[str] = Field(None, description="Assigned asset id")
    status: str = Field(..., description="Current status")
    admin_notes: Optional[str] = Field(None, description="Admin notes")
    requested_at: datetime = Field(..., description="When requested")
    user: Optional[UserResponse] = Field(None, description="Related user details")
    asset: Optional[AssetResponse] = Field(None, description="Mapped asset upon approval")

# Rebuild models
UserResponse.model_rebuild()
AssetCategoryResponse.model_rebuild()
AssetResponse.model_rebuild()
AssignmentResponse.model_rebuild()
RequestResponse.model_rebuild()

class AuditLogResponse(SystemBaseModel):
    id: str
    action: str
    performed_by_id: Optional[str]
    timestamp: datetime
    performed_by: Optional[UserResponse]

# -----------------
# Auth Schemas
# -----------------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
