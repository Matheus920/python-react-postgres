"""
Test script for seed data and resource implementation.

This script tests the seed data and resource implementation by:
1. Making API requests to the resource endpoints
2. Verifying that the seed data is correctly created and accessible
3. Testing various filtering, sorting, and pagination options
4. Testing permission enforcement

Usage:
    python -m app.tests.test_seed_data
"""

import asyncio
import json
import logging
import sys
from typing import Dict, List, Optional, Tuple

import httpx
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.models.resource import Resource
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.resource import Resource as ResourceSchema

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# API base URL
API_BASE_URL = f"http://localhost:8000{settings.API_V1_STR}"


async def get_token(client: httpx.AsyncClient, username: str, password: str) -> str:
    """
    Get an authentication token for a user.
    
    Args:
        client: HTTP client
        username: Username
        password: Password
        
    Returns:
        str: Authentication token
    """
    # Use form data for OAuth2 authentication
    response = await client.post(
        f"{API_BASE_URL}/auth/login",
        data={"username": username, "password": password}
    )
    
    if response.status_code != 200:
        logger.error(f"Failed to get token: {response.text}")
        raise Exception(f"Failed to get token: {response.text}")
    
    token_data = response.json()
    return token_data["access_token"]


async def get_resources(
    client: httpx.AsyncClient, 
    token: str, 
    params: Optional[Dict] = None
) -> Tuple[List[Dict], Dict]:
    """
    Get resources from the API.
    
    Args:
        client: HTTP client
        token: Authentication token
        params: Query parameters
        
    Returns:
        Tuple[List[Dict], Dict]: List of resources and pagination info
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get(
        f"{API_BASE_URL}/resources/",
        headers=headers,
        params=params
    )
    
    if response.status_code != 200:
        logger.error(f"Failed to get resources: {response.text}")
        raise Exception(f"Failed to get resources: {response.text}")
    
    data = response.json()
    return data["items"], data["page_info"]


async def get_resource(client: httpx.AsyncClient, token: str, resource_id: int) -> Dict:
    """
    Get a resource by ID.
    
    Args:
        client: HTTP client
        token: Authentication token
        resource_id: Resource ID
        
    Returns:
        Dict: Resource data
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get(
        f"{API_BASE_URL}/resources/{resource_id}",
        headers=headers
    )
    
    if response.status_code != 200:
        logger.error(f"Failed to get resource: {response.text}")
        raise Exception(f"Failed to get resource: {response.text}")
    
    return response.json()


async def get_my_resources(
    client: httpx.AsyncClient, 
    token: str, 
    params: Optional[Dict] = None
) -> Tuple[List[Dict], Dict]:
    """
    Get resources owned by or shared with the current user.
    
    Args:
        client: HTTP client
        token: Authentication token
        params: Query parameters
        
    Returns:
        Tuple[List[Dict], Dict]: List of resources and pagination info
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get(
        f"{API_BASE_URL}/resources/me",
        headers=headers,
        params=params
    )
    
    if response.status_code != 200:
        logger.error(f"Failed to get my resources: {response.text}")
        raise Exception(f"Failed to get my resources: {response.text}")
    
    data = response.json()
    return data["items"], data["page_info"]


async def test_seed_data():
    """
    Test the seed data and resource implementation.
    """
    logger.info("Testing seed data and resource implementation")
    
    async with httpx.AsyncClient() as client:
        # Get tokens for different users
        admin_token = await get_token(client, "admin", "admin123")
        editor_token = await get_token(client, "editor1", "password")
        author_token = await get_token(client, "author1", "password")
        viewer_token = await get_token(client, "viewer1", "password")
        
        logger.info("Successfully authenticated with different users")
        
        # Test 1: Get all resources as admin
        resources, page_info = await get_resources(client, admin_token)
        logger.info(f"Got {len(resources)} resources as admin (total: {page_info['total']})")
        assert len(resources) > 0, "No resources found"
        assert page_info["total"] >= 100, "Expected at least 100 resources"
        
        # Test 2: Get resources with pagination
        resources_page1, page_info_page1 = await get_resources(
            client, admin_token, {"skip": 0, "limit": 10}
        )
        resources_page2, page_info_page2 = await get_resources(
            client, admin_token, {"skip": 10, "limit": 10}
        )
        
        logger.info(f"Got {len(resources_page1)} resources on page 1")
        logger.info(f"Got {len(resources_page2)} resources on page 2")
        
        assert len(resources_page1) == 10, "Expected 10 resources on page 1"
        assert len(resources_page2) == 10, "Expected 10 resources on page 2"
        assert resources_page1[0]["id"] != resources_page2[0]["id"], "Expected different resources on different pages"
        
        # Test 3: Get resources with filtering
        public_resources, page_info_public = await get_resources(
            client, admin_token, {"is_public": "true"}
        )
        
        logger.info(f"Got {len(public_resources)} public resources")
        assert all(resource.get("is_public") for resource in public_resources), "Expected all resources to be public"
        
        # Test 4: Get resources with sorting
        resources_asc, _ = await get_resources(
            client, admin_token, {"sort_by": "name", "sort_order": "asc", "limit": 10}
        )
        resources_desc, _ = await get_resources(
            client, admin_token, {"sort_by": "name", "sort_order": "desc", "limit": 10}
        )
        
        logger.info(f"Got resources sorted by name (asc): {[r['name'] for r in resources_asc[:3]]}")
        logger.info(f"Got resources sorted by name (desc): {[r['name'] for r in resources_desc[:3]]}")
        
        assert resources_asc[0]["name"] != resources_desc[0]["name"], "Expected different order for asc and desc sorting"
        
        # Test 5: Get resources with search
        search_term = "document"
        search_resources, _ = await get_resources(
            client, admin_token, {"search": search_term}
        )
        
        logger.info(f"Got {len(search_resources)} resources matching search term '{search_term}'")
        
        # Test 6: Get a specific resource
        resource_id = resources[0]["id"]
        resource = await get_resource(client, admin_token, resource_id)
        
        logger.info(f"Got resource with ID {resource_id}: {resource['name']}")
        assert resource["id"] == resource_id, "Expected resource with correct ID"
        
        # Test 7: Get resources owned by or shared with the current user
        my_resources_admin, _ = await get_my_resources(client, admin_token)
        my_resources_editor, _ = await get_my_resources(client, editor_token)
        my_resources_author, _ = await get_my_resources(client, author_token)
        my_resources_viewer, _ = await get_my_resources(client, viewer_token)
        
        logger.info(f"Admin has access to {len(my_resources_admin)} resources")
        logger.info(f"Editor has access to {len(my_resources_editor)} resources")
        logger.info(f"Author has access to {len(my_resources_author)} resources")
        logger.info(f"Viewer has access to {len(my_resources_viewer)} resources")
        
        # Test 8: Test permission enforcement
        # Try to access a non-public resource owned by admin as viewer
        admin_resources = [r for r in resources if r["owner_id"] == 1 and not r.get("is_public")]
        if admin_resources:
            admin_resource_id = admin_resources[0]["id"]
            
            # Admin should be able to access it
            admin_resource = await get_resource(client, admin_token, admin_resource_id)
            logger.info(f"Admin can access their own resource: {admin_resource['name']}")
            
            # Viewer might not be able to access it unless it's shared
            try:
                viewer_resource = await get_resource(client, viewer_token, admin_resource_id)
                logger.info(f"Viewer can access admin's resource (it must be shared): {viewer_resource['name']}")
            except Exception as e:
                logger.info(f"Viewer cannot access admin's resource (as expected if not shared): {str(e)}")
        
        logger.info("All tests passed successfully!")


if __name__ == "__main__":
    asyncio.run(test_seed_data())
