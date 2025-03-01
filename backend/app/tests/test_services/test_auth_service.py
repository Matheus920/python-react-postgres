import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import auth_service


@pytest.mark.asyncio
async def test_register_user(db_session: AsyncSession):
    """Test user registration."""
    # Create a test user
    user_in = UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123",
        first_name="Test",
        last_name="User",
    )
    
    # Register the user
    user = await auth_service.register_user(db=db_session, user_in=user_in)
    
    # Check that the user was created correctly
    assert user.email == user_in.email
    assert user.username == user_in.username
    assert user.first_name == user_in.first_name
    assert user.last_name == user_in.last_name
    assert verify_password("password123", user.hashed_password)
    assert user.is_active is True
    assert user.is_admin is False


@pytest.mark.asyncio
async def test_authenticate_user(db_session: AsyncSession):
    """Test user authentication."""
    # Create a test user
    user_in = UserCreate(
        email="auth@example.com",
        username="authuser",
        password="password123",
        first_name="Auth",
        last_name="User",
    )
    
    # Register the user
    await auth_service.register_user(db=db_session, user_in=user_in)
    
    # Test authentication with username
    user = await auth_service.authenticate_user(
        db=db_session, username="authuser", password="password123"
    )
    assert user is not None
    assert user.username == "authuser"
    
    # Test authentication with email
    user = await auth_service.authenticate_user(
        db=db_session, username="auth@example.com", password="password123"
    )
    assert user is not None
    assert user.email == "auth@example.com"
    
    # Test authentication with wrong password
    user = await auth_service.authenticate_user(
        db=db_session, username="authuser", password="wrongpassword"
    )
    assert user is None
    
    # Test authentication with non-existent user
    user = await auth_service.authenticate_user(
        db=db_session, username="nonexistent", password="password123"
    )
    assert user is None


@pytest.mark.asyncio
async def test_create_access_token():
    """Test access token creation."""
    # Create an access token
    token = auth_service.create_access_token(user_id=1)
    
    # Check that the token is a string
    assert isinstance(token, str)
    assert len(token) > 0
