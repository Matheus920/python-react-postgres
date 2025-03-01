from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


# Shared properties
class UserBase(BaseModel):
    """
    Base user schema with shared properties.
    """
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False
    first_name: Optional[str] = None
    last_name: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    email: EmailStr
    username: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    """
    Schema for updating a user.
    """
    password: Optional[str] = None


# Properties to return via API
class User(UserBase):
    """
    Schema for returning a user.
    """
    id: int
    email: EmailStr
    username: str
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True


# Properties to return via API for the current user
class UserInDB(User):
    """
    Schema for returning a user with additional database information.
    """
    hashed_password: str
    
    class Config:
        from_attributes = True


# Properties to return via API for a list of users
class UserList(BaseModel):
    """
    Schema for returning a list of users.
    """
    users: List[User]
    total: int
