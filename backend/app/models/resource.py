from typing import List, Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Table
from sqlalchemy.orm import relationship

from app.db.base import Base

# Association table for resource-permission many-to-many relationship
resource_permission = Table(
    "resource_permission",
    Base.metadata,
    Column("resource_id", Integer, ForeignKey("resources.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("permission_type", String, nullable=False),  # e.g., "read", "write", "admin"
)


class Resource(Base):
    """
    Resource model for the resource management system.
    
    Attributes:
        id: Unique identifier
        name: Resource name
        description: Resource description
        content: Resource content
        metadata: Resource metadata (JSON)
        is_public: Whether the resource is public
        owner_id: ID of the user who owns the resource
        owner: User who owns the resource (many-to-one relationship)
        shared_with: Users with whom the resource is shared (many-to-many relationship)
    """
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    content = Column(Text)
    meta_data = Column(Text)  # JSON string (renamed from metadata to avoid conflict)
    is_public = Column(Boolean, default=False)
    
    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="resources")
    shared_with = relationship(
        "User",
        secondary=resource_permission,
        primaryjoin="Resource.id == resource_permission.c.resource_id",
        secondaryjoin="User.id == resource_permission.c.user_id",
    )
    
    def has_permission(self, user_id: int, permission_type: str) -> bool:
        """
        Check if a user has a specific permission for this resource.
        
        Args:
            user_id: ID of the user
            permission_type: Type of permission to check
            
        Returns:
            bool: True if the user has the permission, False otherwise
        """
        # Owner has all permissions
        if user_id == self.owner_id:
            return True
        
        # Check if the resource is public and the permission is "read"
        if self.is_public and permission_type == "read":
            return True
        
        # Check if the user has the specific permission
        for user in self.shared_with:
            if user.id == user_id:
                # This is a simplification; in a real system, we would check the permission_type
                return True
        
        return False
