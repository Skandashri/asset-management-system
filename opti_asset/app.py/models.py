import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class Employee(Base):
    """
    Represents an employee in the system.
    
    Attributes:
        id (UUID): Primary key for the employee.
        name (str): Full name of the employee.
        email (str): Unique email address.
        department (str): Department the employee belongs to.
        is_active (bool): Flag for soft deletion.
        created_at (datetime): Timestamp of creation.
        assignments (list[Assignment]): Assets assigned to the employee.
    """
    __tablename__ = "employees"

    # Primary key using PostgreSQL UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Required employee name
    name = Column(String, nullable=False)
    
    # Unique and indexed email address for constraint fulfillment
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Department the employee belongs to
    department = Column(String, nullable=True)
    
    # Soft delete flag: True if active, False if softly deleted
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamp for creation
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to Assignment
    assignments = relationship("Assignment", back_populates="employee", cascade="all, delete-orphan")


class Asset(Base):
    """
    Represents a physical or digital asset in the system.
    
    Attributes:
        id (UUID): Primary key for the asset.
        asset_tag (str): Unique tag for the asset.
        name (str): Name of the asset.
        description (str): Detailed description of the asset.
        is_available (bool): Flag indicating if the asset can be assigned.
        is_active (bool): Flag for soft deletion.
        created_at (datetime): Timestamp of creation.
        assignments (list[Assignment]): Assignment history of the asset.
    """
    __tablename__ = "assets"

    # Primary key using PostgreSQL UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Unique and indexed asset tag for constraint fulfillment
    asset_tag = Column(String, unique=True, index=True, nullable=False)
    
    # Name of the asset
    name = Column(String, nullable=True)
    
    # Description of the asset
    description = Column(String, nullable=True)
    
    # Flag indicating if the asset is currently available for assignment
    is_available = Column(Boolean, default=True, nullable=False)
    
    # Soft delete flag: True if active, False if softly deleted
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamp for creation
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to Assignment
    assignments = relationship("Assignment", back_populates="asset", cascade="all, delete-orphan")


class Assignment(Base):
    """
    Represents an assignment of an asset to an employee.
    
    Attributes:
        id (UUID): Primary key for the assignment.
        employee_id (UUID): Foreign key linking to the assigned employee.
        asset_id (UUID): Foreign key linking to the assigned asset.
        assigned_at (datetime): Timestamp when the asset was assigned.
        returned_at (datetime): Timestamp when the asset was returned (if applicable).
        employee (Employee): Relationship to the assigned employee.
        asset (Asset): Relationship to the assigned asset.
    """
    __tablename__ = "assignments"

    # Primary key using PostgreSQL UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Foreign key referring to the employee who is assigned the asset
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False, index=True)
    
    # Foreign key referring to the asset that is being assigned
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    
    # Timestamp indicating when the asset was assigned to the employee
    assigned_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Timestamp indicating when the asset was returned; nullable if still holding the asset
    returned_at = Column(DateTime, nullable=True)

    # Relationship linking back to the employee model
    employee = relationship("Employee", back_populates="assignments")
    
    # Relationship linking back to the asset model
    asset = relationship("Asset", back_populates="assignments")
