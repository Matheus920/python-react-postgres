from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.models.user import User
from app.repositories.user import user_repository
from app.schemas.auth import TokenPayload
from app.schemas.user import UserCreate


class AuthService:
    """
    Service for authentication operations.
    """
    
    async def authenticate_user(
        self, db: AsyncSession, username: str, password: str
    ) -> Optional[User]:
        """
        Authenticate a user.
        
        Args:
            db: Database session
            username: Username or email
            password: Password
            
        Returns:
            Optional[User]: User if authentication succeeds, None otherwise
        """
        user = await user_repository.get_by_email_or_username(
            db, email_or_username=username
        )
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_access_token(
        self, user_id: int, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token.
        
        Args:
            user_id: User ID
            expires_delta: Optional expiration time delta
            
        Returns:
            str: JWT access token
        """
        return create_access_token(
            subject=str(user_id), expires_delta=expires_delta
        )
    
    async def register_user(
        self, db: AsyncSession, user_in: UserCreate
    ) -> User:
        """
        Register a new user.
        
        Args:
            db: Database session
            user_in: User creation schema
            
        Returns:
            User: Created user
            
        Raises:
            HTTPException: If the email or username is already registered
        """
        # Check if email is already registered
        user = await user_repository.get_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        # Check if username is already registered
        user = await user_repository.get_by_username(db, username=user_in.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )
        
        # Create new user
        user = await user_repository.create_with_password(db, obj_in=user_in)
        return user


# Create a singleton instance
auth_service = AuthService()
