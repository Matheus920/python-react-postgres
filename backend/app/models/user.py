from typing import List, Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.db.base import Base

# Association table for user-role many-to-many relationship
user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)


class User(Base):
    """
    User model for authentication and authorization.
    
    Attributes:
        id: Unique identifier
        email: User's email address (unique)
        username: User's username (unique)
        hashed_password: Hashed password
        first_name: User's first name
        last_name: User's last name
        is_active: Whether the user is active
        is_admin: Whether the user is an admin
        roles: User's roles (many-to-many relationship)
        resources: Resources owned by the user (one-to-many relationship)
    """
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Relationships
    roles = relationship("Role", secondary=user_role, back_populates="users")
    resources = relationship("Resource", back_populates="owner")
    
    @property
    def full_name(self) -> str:
        """
        Get the user's full name.
        
        Returns:
            str: Full name (first name + last name)
        """
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
