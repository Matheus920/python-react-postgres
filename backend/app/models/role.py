from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.models.user import user_role

# Association table for role-permission many-to-many relationship
role_permission = Table(
    "role_permission",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)


class Role(Base):
    """
    Role model for role-based access control.
    
    Attributes:
        id: Unique identifier
        name: Role name (unique)
        description: Role description
        users: Users with this role (many-to-many relationship)
        permissions: Permissions associated with this role (many-to-many relationship)
    """
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    
    # Relationships
    users = relationship("User", secondary=user_role, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permission, back_populates="roles")


class Permission(Base):
    """
    Permission model for role-based access control.
    
    Attributes:
        id: Unique identifier
        name: Permission name (unique)
        description: Permission description
        roles: Roles with this permission (many-to-many relationship)
    """
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    
    # Relationships
    roles = relationship("Role", secondary=role_permission, back_populates="permissions")
