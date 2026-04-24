import uuid
from datetime import datetime
import json

from sqlalchemy import Column, String, Boolean, DateTime, Date, Float, ForeignKey, Enum, Text, CheckConstraint, Integer
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.types import TypeDecorator

class JSONList(TypeDecorator):
    """Custom type for storing lists as JSON in SQLite"""
    impl = Text
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None
    
    def process_result_value(self, value, dialect):
        if value is not None:
            if isinstance(value, str):
                return json.loads(value)
            return value
        return []

Base = declarative_base()

class Role(Base):
    """
    Role definitions within the system (e.g., Admin, Regular User).
    """
    __tablename__ = "roles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    permissions = Column(JSONList, default=list, nullable=False)

    users = relationship("User", foreign_keys="User.role_id", back_populates="role")

class User(Base):
    """
    System user (previously Employee) mapped to roles.
    Supports multiple roles for role-switching functionality.
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    role_id = Column(String, ForeignKey("roles.id"), nullable=False)
    secondary_role_id = Column(String, ForeignKey("roles.id", name="fk_user_secondary_role"), nullable=True)  # For role switching
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    department = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    role = relationship("Role", foreign_keys=[role_id], back_populates="users")
    secondary_role_rel = relationship("Role", foreign_keys=[secondary_role_id])
    assignments = relationship("Assignment", back_populates="user", cascade="all, delete-orphan")
    reports = relationship("AssetReport", back_populates="reported_by", cascade="all, delete-orphan")
    requests = relationship("Request", back_populates="user", cascade="all, delete-orphan")

class AssetCategory(Base):
    """
    Categorical grouping of assets for inventory monitoring.
    """
    __tablename__ = "asset_categories"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    # total_quantity and available_quantity can be dynamically computed from Asset relations
    # or stored directly as counters if preferred. The user asked for columns:
    total_quantity = Column(Integer, default=0, nullable=False)
    available_quantity = Column(Integer, default=0, nullable=False)

    assets = relationship("Asset", back_populates="category_rel", cascade="all, delete-orphan")

class Asset(Base):
    """
    Inventory item. Tracks its current explicitly bounded status.
    """
    __tablename__ = "assets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    asset_tag = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    category_id = Column(String, ForeignKey("asset_categories.id"), nullable=True)
    purchase_date = Column(Date, nullable=True)
    cost = Column(Float, nullable=True)
    image_url = Column(String, nullable=True)
    document_url = Column(String, nullable=True)
    vendor = Column(String, nullable=True)
    location = Column(String, nullable=True)
    status = Column(String, default="Available", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    category_rel = relationship("AssetCategory", back_populates="assets")
    assignments = relationship("Assignment", back_populates="asset", cascade="all, delete-orphan")
    status_logs = relationship("AssetStatusLog", back_populates="asset", cascade="all, delete-orphan")

    @property
    def assigned_to(self):
        for assignment in self.assignments:
            if assignment.return_date is None:
                return assignment.user
        return None

class Assignment(Base):
    """
    Tracks assignments mapping Users securely to Assets.
    """
    __tablename__ = "assignments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    asset_id = Column(String, ForeignKey("assets.id"), nullable=False, index=True)
    assigned_date = Column(DateTime, default=datetime.utcnow, nullable=False) # Changed from assigned_at per requirement
    return_date = Column(DateTime, nullable=True) # Changed from returned_at per requirement

    user = relationship("User", back_populates="assignments")
    asset = relationship("Asset", back_populates="assignments")

class AssetStatusLog(Base):
    """
    Audit log of status changes for an explicitly bounded constraint on an asset.
    """
    __tablename__ = "asset_status_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    asset_id = Column(String, ForeignKey("assets.id"), nullable=False, index=True)
    old_status = Column(String, nullable=True)
    new_status = Column(String, nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    asset = relationship("Asset", back_populates="status_logs")

class AssetReport(Base):
    """
    Reports for damaged or problematic assets submitted by users.
    """
    __tablename__ = "asset_reports"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    asset_id = Column(String, ForeignKey("assets.id"), nullable=False, index=True)
    reported_by_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    report_type = Column(String, nullable=False)  # Damaged, Lost, Stolen, Maintenance Required
    description = Column(Text, nullable=False)
    severity = Column(String, default="Medium")  # Low, Medium, High, Critical
    status = Column(String, default="Pending")  # Pending, Under Review, Resolved, Rejected
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    admin_notes = Column(Text, nullable=True)

    asset = relationship("Asset", back_populates="reports")
    reported_by = relationship("User", back_populates="reports")

# Add relationship to Asset model
Asset.reports = relationship("AssetReport", back_populates="asset", cascade="all, delete-orphan")

class Request(Base):
    """
    Requests for equipment/assets from users.
    """
    __tablename__ = "requests"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    asset_id = Column(String, ForeignKey("assets.id"), nullable=True, index=True)
    item_name = Column(String, nullable=False)
    item_type = Column(String, nullable=False) # Equipment, Accessory, Software, Other
    notes = Column(Text, nullable=True)
    status = Column(String, default="Pending", nullable=False) # Pending, Approved, Rejected
    admin_notes = Column(Text, nullable=True)
    requested_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        CheckConstraint(status.in_(['Pending', 'Approved', 'Rejected']), name="request_status_check"),
    )

    user = relationship("User", back_populates="requests")
    asset = relationship("Asset")

class AuditLog(Base):
    """
    Audit log tracking actions across the system.
    """
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    action = Column(String, nullable=False)
    performed_by_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    performed_by = relationship("User")
