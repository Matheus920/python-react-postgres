from typing import List, Optional, Dict, Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserUpdate
from app.utils.caching import cached
from app.utils.pagination import PaginationParams, create_page, Page


class UserService:
    """
    Service for user operations.
    """
    
    @cached()
    async def get_users(
        self,
        db: AsyncSession,
        *,
        pagination: PaginationParams
    ) -> Page[User]:
        """
        Get users with pagination.
        
        Args:
            db: Database session
            pagination: Pagination parameters
            
        Returns:
            Page[User]: Paginated users
        """
        # Get users
        users = await user_repository.get_multi(
            db, skip=pagination.skip, limit=pagination.limit
        )
        
        # Count total users
        total = await user_repository.count(db)
        
        # Create paginated response
        return create_page(users, total, pagination)
    
    async def get_user(
        self,
        db: AsyncSession,
        *,
        user_id: int
    ) -> Optional[User]:
        """
        Get a user by ID.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Optional[User]: User if found, None otherwise
            
        Raises:
            HTTPException: If the user is not found
        """
        user = await user_repository.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
    
    async def create_user(
        self,
        db: AsyncSession,
        *,
        obj_in: UserCreate
    ) -> User:
        """
        Create a new user.
        
        Args:
            db: Database session
            obj_in: User creation schema
            
        Returns:
            User: Created user
            
        Raises:
            HTTPException: If the email or username is already registered
        """
        # Check if email is already registered
        user = await user_repository.get_by_email(db, email=obj_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        # Check if username is already registered
        user = await user_repository.get_by_username(db, username=obj_in.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        
        # Create new user
        return await user_repository.create_with_password(db, obj_in=obj_in)
    
    async def update_user(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        obj_in: UserUpdate,
        current_user: User
    ) -> User:
        """
        Update a user.
        
        Args:
            db: Database session
            user_id: User ID
            obj_in: User update schema
            current_user: Current user
            
        Returns:
            User: Updated user
            
        Raises:
            HTTPException: If the user is not found or the current user is not authorized
        """
        user = await user_repository.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        # Check if the current user is the user being updated or an admin
        if user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        
        # Update user
        return await user_repository.update_with_password(db, db_obj=user, obj_in=obj_in)
    
    async def delete_user(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        current_user: User
    ) -> User:
        """
        Delete a user.
        
        Args:
            db: Database session
            user_id: User ID
            current_user: Current user
            
        Returns:
            User: Deleted user
            
        Raises:
            HTTPException: If the user is not found or the current user is not authorized
        """
        user = await user_repository.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        # Check if the current user is the user being deleted or an admin
        if user_id != current_user.id and not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        
        # Delete user
        return await user_repository.remove(db, id=user_id)
    
    async def get_me(
        self,
        db: AsyncSession,
        *,
        current_user: User
    ) -> User:
        """
        Get the current user.
        
        Args:
            db: Database session
            current_user: Current user
            
        Returns:
            User: Current user
        """
        return current_user


# Create a singleton instance
user_service = UserService()
