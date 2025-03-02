#!/usr/bin/env python3
"""
Script to create a regular (non-admin) test user for the application.
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

# Regular test user credentials
TEST_EMAIL = "regular@example.com"
TEST_USERNAME = "regularuser"
TEST_PASSWORD = "password123"  # In a real app, use a secure password


async def create_regular_user():
    """
    Create a regular (non-admin) test user with sample resources.
    """
    logger.info("Creating regular test user")
    
    async with AsyncSessionLocal() as db:
        # Check if regular user already exists
        result = await db.execute(select(User).where(User.username == TEST_USERNAME))
        regular_user = result.scalars().first()
        
        if regular_user:
            logger.info(f"Regular user '{TEST_USERNAME}' already exists")
            # Create a sample resource for the user
            await create_sample_resource(db, regular_user)
            return
        
        # Get regular role if it exists
        result = await db.execute(select(Role).where(Role.name == "user"))
        user_role = result.scalars().first()
        
        # Create regular user
        regular_user = User(
            email=TEST_EMAIL,
            username=TEST_USERNAME,
            hashed_password=get_password_hash(TEST_PASSWORD),
            first_name="Regular",
            last_name="User",
            is_active=True,
            is_admin=False  # This is a regular user, not an admin
        )
        
        # Add user role if it exists
        if user_role:
            regular_user.roles = [user_role]
        
        db.add(regular_user)
        await db.commit()
        
        # Create a sample resource for the user
        await create_sample_resource(db, regular_user)
        
        logger.info(f"Regular user '{TEST_USERNAME}' created successfully")
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
        name="Regular User Resource",
        description="A sample resource created by a regular user",
        content="This is a sample resource content created by a regular user for testing purposes.",
        meta_data=json.dumps({
            "type": "document",
            "tags": ["sample", "regular", "test"],
            "status": "draft",
            "created_date": "2023-01-02T00:00:00",
            "modified_date": "2023-01-02T00:00:00",
            "version": "1.0",
            "is_public": False,
        }),
        is_public=False,  # Private resource
        owner_id=user.id
    )
    
    db.add(sample_resource)
    await db.commit()
    
    logger.info(f"Created sample resource for user {user.username}")


if __name__ == "__main__":
    asyncio.run(create_regular_user())
