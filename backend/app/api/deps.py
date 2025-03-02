from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.session import get_db
from app.models.user import User
from app.repositories.user import user_repository
from app.schemas.auth import TokenPayload

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


import logging

# Configure logging
logger = logging.getLogger(__name__)

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    Get the current authenticated user.
    
    Args:
        db: Database session
        token: JWT token
        
    Returns:
        User: Current user
        
    Raises:
        HTTPException: If authentication fails
    """
    logger.info(f"Authenticating user with token: {token[:10]}...")
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        logger.info(f"Token decoded successfully: {payload}")
        token_data = TokenPayload(**payload)
        logger.info(f"Token data validated: {token_data}")
    except (JWTError, ValidationError) as e:
        logger.error(f"Token validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Convert token_data.sub (string) to integer for database query
    user_id = int(token_data.sub)
    logger.info(f"Looking up user with ID: {user_id}")
    
    user = await user_repository.get(db, id=user_id)
    if not user:
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    logger.info(f"User authenticated: {user.username} (ID: {user.id})")
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get the current active user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Current active user
        
    Raises:
        HTTPException: If the user is inactive
    """
    logger.info(f"Checking if user {current_user.username} (ID: {current_user.id}) is active")
    
    if not current_user.is_active:
        logger.error(f"User {current_user.username} (ID: {current_user.id}) is inactive")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    
    logger.info(f"User {current_user.username} (ID: {current_user.id}) is active")
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Get the current admin user.
    
    Args:
        current_user: Current active user
        
    Returns:
        User: Current admin user
        
    Raises:
        HTTPException: If the user is not an admin
    """
    logger.info(f"Checking if user {current_user.username} (ID: {current_user.id}) is admin")
    
    if not current_user.is_admin:
        logger.error(f"User {current_user.username} (ID: {current_user.id}) is not admin")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    logger.info(f"User {current_user.username} (ID: {current_user.id}) is admin")
    return current_user
