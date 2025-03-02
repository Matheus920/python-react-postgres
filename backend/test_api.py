#!/usr/bin/env python3
"""
Script to test the API endpoints.
"""
import asyncio
import logging
import json
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API base URL
BASE_URL = "http://localhost:8000/api/v1"

# Test user credentials
TEST_USERNAME = "testuser"
TEST_PASSWORD = "password123"


async def test_api():
    """
    Test the API endpoints.
    """
    logger.info("Testing API endpoints")
    
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
            f"{BASE_URL}/resources",
            headers=headers,
        )
        
        if resources_response.status_code != 200:
            logger.error(f"Get resources failed: {resources_response.status_code} {resources_response.text}")
            return
        
        logger.info(f"Get resources successful: {resources_response.status_code}")
        resources_data = resources_response.json()
        logger.info(f"Resources data: {json.dumps(resources_data, indent=2)}")


if __name__ == "__main__":
    asyncio.run(test_api())
