#!/usr/bin/env python3
"""
Script to test authentication and resource access.
This script will help diagnose the 401 Unauthorized error when accessing resources.
"""
import asyncio
import logging
import json
import httpx
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

# Test user credentials
TEST_USERNAME = "testuser"
TEST_PASSWORD = "password123"


async def test_auth_resource(resource_id=None):
    """
    Test authentication and resource access.
    
    Args:
        resource_id: Optional resource ID to test. If not provided, will test all resources.
    """
    logger.info("Testing authentication and resource access")
    
    # Create a client that follows redirects
    async with httpx.AsyncClient(follow_redirects=True) as client:
        # Test login
        logger.info("Testing login endpoint")
        login_data = {
            "username": TEST_USERNAME,
            "password": TEST_PASSWORD,
        }
        login_response = await client.post(
            f"{BASE_URL}/auth/login",
            data=login_data,
        )
        
        if login_response.status_code != 200:
            logger.error(f"Login failed: {login_response.status_code} {login_response.text}")
            return
        
        logger.info(f"Login successful: {login_response.status_code}")
        token_data = login_response.json()
        logger.info(f"Token data: {token_data}")
        
        # Set the token for subsequent requests
        headers = {
            "Authorization": f"Bearer {token_data['access_token']}",
        }
        
        # Test get current user
        logger.info("Testing get current user endpoint")
        user_response = await client.get(
            f"{BASE_URL}/users/me",
            headers=headers,
        )
        
        if user_response.status_code != 200:
            logger.error(f"Get current user failed: {user_response.status_code} {user_response.text}")
            return
        
        logger.info(f"Get current user successful: {user_response.status_code}")
        user_data = user_response.json()
        logger.info(f"User data: {json.dumps(user_data, indent=2)}")
        
        # Test get resources
        logger.info("Testing get resources endpoint")
        resources_response = await client.get(
            f"{BASE_URL}/resources/",  # Note the trailing slash
            headers=headers,
        )
        
        if resources_response.status_code != 200:
            logger.error(f"Get resources failed: {resources_response.status_code} {resources_response.text}")
            return
        
        logger.info(f"Get resources successful: {resources_response.status_code}")
        resources_data = resources_response.json()
        logger.info(f"Resources count: {len(resources_data.get('items', []))}")
        
        # If a specific resource ID is provided, test that resource
        if resource_id:
            logger.info(f"Testing get resource endpoint for resource ID {resource_id}")
            resource_response = await client.get(
                f"{BASE_URL}/resources/{resource_id}/",  # Note the trailing slash
                headers=headers,
            )
            
            if resource_response.status_code != 200:
                logger.error(f"Get resource failed: {resource_response.status_code} {resource_response.text}")
                return
            
            logger.info(f"Get resource successful: {resource_response.status_code}")
            resource_data = resource_response.json()
            logger.info(f"Resource data: {json.dumps(resource_data, indent=2)}")
        else:
            # Test the first resource if available
            resources = resources_data.get('items', [])
            if resources:
                resource_id = resources[0]['id']
                logger.info(f"Testing get resource endpoint for first resource (ID: {resource_id})")
                resource_response = await client.get(
                    f"{BASE_URL}/resources/{resource_id}/",  # Note the trailing slash
                    headers=headers,
                )
                
                if resource_response.status_code != 200:
                    logger.error(f"Get resource failed: {resource_response.status_code} {resource_response.text}")
                    return
                
                logger.info(f"Get resource successful: {resource_response.status_code}")
                resource_data = resource_response.json()
                logger.info(f"Resource data: {json.dumps(resource_data, indent=2)}")
            else:
                logger.warning("No resources found to test individual resource access")


if __name__ == "__main__":
    # If a resource ID is provided as a command-line argument, use it
    resource_id = int(sys.argv[1]) if len(sys.argv) > 1 else None
    asyncio.run(test_auth_resource(resource_id))
