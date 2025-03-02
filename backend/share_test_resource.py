#!/usr/bin/env python3
"""
Script to share a resource between the admin user and the regular user.
This demonstrates the role-based access control functionality.
"""
import asyncio
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.models.resource import Resource, resource_permission

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test user credentials from create_test_user.py and create_regular_user.py
ADMIN_USERNAME = "testuser"
REGULAR_USERNAME = "regularuser"


async def share_test_resource():
    """
    Share a resource from the admin user to the regular user.
    """
    logger.info("Sharing test resource between users")
    
    async with AsyncSessionLocal() as db:
        # Get admin user
        result = await db.execute(select(User).where(User.username == ADMIN_USERNAME))
        admin_user = result.scalars().first()
        
        if not admin_user:
            logger.error(f"Admin user '{ADMIN_USERNAME}' not found. Please run create_test_user.py first.")
            return
        
        # Get regular user
        result = await db.execute(select(User).where(User.username == REGULAR_USERNAME))
        regular_user = result.scalars().first()
        
        if not regular_user:
            logger.error(f"Regular user '{REGULAR_USERNAME}' not found. Please run create_regular_user.py first.")
            return
        
        # Get a resource owned by the admin user
        result = await db.execute(select(Resource).where(Resource.owner_id == admin_user.id))
        admin_resource = result.scalars().first()
        
        if not admin_resource:
            logger.error(f"No resources found for admin user. Please run create_test_user.py first.")
            return
        
        # Check if the resource is already shared with the regular user
        stmt = select(resource_permission).where(
            (resource_permission.c.resource_id == admin_resource.id) &
            (resource_permission.c.user_id == regular_user.id)
        )
        result = await db.execute(stmt)
        existing_permission = result.first()
        
        if existing_permission:
            logger.info(f"Resource '{admin_resource.name}' is already shared with '{regular_user.username}'")
            return
        
        # Share the resource with the regular user
        stmt = resource_permission.insert().values(
            resource_id=admin_resource.id,
            user_id=regular_user.id,
            permission_type="read"
        )
        await db.execute(stmt)
        await db.commit()
        
        logger.info(f"Shared resource '{admin_resource.name}' with user '{regular_user.username}'")
        
        # Create a resource owned by the regular user
        result = await db.execute(select(Resource).where(Resource.owner_id == regular_user.id))
        regular_resource = result.scalars().first()
        
        if not regular_resource:
            logger.error(f"No resources found for regular user. Please run create_regular_user.py first.")
            return
        
        # Check if the resource is already shared with the admin user
        stmt = select(resource_permission).where(
            (resource_permission.c.resource_id == regular_resource.id) &
            (resource_permission.c.user_id == admin_user.id)
        )
        result = await db.execute(stmt)
        existing_permission = result.first()
        
        if existing_permission:
            logger.info(f"Resource '{regular_resource.name}' is already shared with '{admin_user.username}'")
            return
        
        # Share the resource with the admin user
        stmt = resource_permission.insert().values(
            resource_id=regular_resource.id,
            user_id=admin_user.id,
            permission_type="read"
        )
        await db.execute(stmt)
        await db.commit()
        
        logger.info(f"Shared resource '{regular_resource.name}' with user '{admin_user.username}'")


if __name__ == "__main__":
    asyncio.run(share_test_resource())
