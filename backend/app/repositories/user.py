from typing import List, Optional, Union, Dict, Any

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """
    Repository for User model.
    """
    
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        """
        Get a user by email.
        
        Args:
            db: Database session
            email: Email address
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_by_username(self, db: AsyncSession, *, username: str) -> Optional[User]:
        """
        Get a user by username.
        
        Args:
            db: Database session
            username: Username
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        query = select(User).where(User.username == username)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_by_email_or_username(
        self, db: AsyncSession, *, email_or_username: str
    ) -> Optional[User]:
        """
        Get a user by email or username.
        
        Args:
            db: Database session
            email_or_username: Email address or username
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        query = select(User).where(
            or_(User.email == email_or_username, User.username == email_or_username)
        )
        result = await db.execute(query)
        return result.scalars().first()
    
    async def create_with_password(
        self, db: AsyncSession, *, obj_in: UserCreate
    ) -> User:
        """
        Create a new user with password hashing.
        
        Args:
            db: Database session
            obj_in: User creation schema
            
        Returns:
            User: Created user
        """
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            is_active=obj_in.is_active,
            is_admin=obj_in.is_admin,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update_with_password(
        self,
        db: AsyncSession,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Update a user with password hashing if password is provided.
        
        Args:
            db: Database session
            db_obj: User to update
            obj_in: User update schema or dictionary
            
        Returns:
            User: Updated user
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        
        return await super().update(db, db_obj=db_obj, obj_in=update_data)
    
    async def authenticate(
        self, db: AsyncSession, *, email_or_username: str, password: str
    ) -> Optional[User]:
        """
        Authenticate a user.
        
        Args:
            db: Database session
            email_or_username: Email address or username
            password: Password
            
        Returns:
            Optional[User]: User if authentication succeeds, None otherwise
        """
        user = await self.get_by_email_or_username(db, email_or_username=email_or_username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    async def is_active(self, user: User) -> bool:
        """
        Check if a user is active.
        
        Args:
            user: User to check
            
        Returns:
            bool: True if the user is active, False otherwise
        """
        return user.is_active
    
    async def is_admin(self, user: User) -> bool:
        """
        Check if a user is an admin.
        
        Args:
            user: User to check
            
        Returns:
            bool: True if the user is an admin, False otherwise
        """
        return user.is_admin


# Create a singleton instance
user_repository = UserRepository(User)
