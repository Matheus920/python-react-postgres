#!/usr/bin/env python3
"""
Script to create a test user for the application.
"""
import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.resource import Resource
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test user credentials
TEST_EMAIL = "test@example.com"
TEST_USERNAME = "testuser"
TEST_PASSWORD = "password123"  # In a real app, use a secure password


async def create_test_user():
    """
    Create a test user with admin privileges and sample resources.
    """
    logger.info("Creating test user")
    
    async with AsyncSessionLocal() as db:
        # Check if test user already exists
        result = await db.execute(select(User).where(User.username == TEST_USERNAME))
        test_user = result.scalars().first()
        
        if test_user:
            logger.info(f"Test user '{TEST_USERNAME}' already exists")
            # Create a sample resource for the user
            await create_sample_resource(db, test_user)
            return
        
        # Get admin role if it exists
        result = await db.execute(select(Role).where(Role.name == "admin"))
        admin_role = result.scalars().first()
        
        # Create test user
        test_user = User(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            hashed_password=get_password_hash(TEST_PASSWORD),
            first_name="Test",
            last_name="User",
            is_active=True,
            is_admin=True
        )
        
        # Add admin role if it exists
        if admin_role:
            test_user.roles = [admin_role]
        
        db.add(test_user)
        await db.commit()
        
        # Create a sample resource for the user
        await create_sample_resource(db, test_user)
        
        logger.info(f"Test user '{TEST_USERNAME}' created successfully")
        logger.info(f"Username: {TEST_USERNAME}")
        logger.info(f"Password: {TEST_PASSWORD}")


async def create_sample_resource(db: AsyncSession, user: User):
    """
    Create a sample resource for the user.
    """
    # Check if user already has resources
    result = await db.execute(select(Resource).where(Resource.owner_id == user.id))
    existing_resources = result.scalars().all()
    
    if existing_resources:
        logger.info(f"User already has {len(existing_resources)} resources")
        return
    
    # Create a sample resource
    sample_resource = Resource(
        name="Sample Resource",
        description="A sample resource for testing",
        content="This is a sample resource content for testing purposes.",
        meta_data=json.dumps({
            "type": "document",
            "tags": ["sample", "test"],
            "status": "published",
            "created_date": "2023-01-01T00:00:00",
            "modified_date": "2023-01-01T00:00:00",
            "version": "1.0",
            "is_public": True,
        }),
        is_public=True,
        owner_id=user.id
    )
    
    db.add(sample_resource)
    await db.commit()
    
    logger.info(f"Created sample resource for user {user.username}")


if __name__ == "__main__":
    asyncio.run(create_test_user())
