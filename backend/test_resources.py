#!/usr/bin/env python3
"""
Script to run the application and test the seed data.

This script:
1. Starts the application in the background
2. Waits for the application to be ready
3. Runs the test script to verify the seed data and resource implementation
4. Shuts down the application

Usage:
    python test_resources.py
"""

import asyncio
import logging
import os
import signal
import subprocess
import sys
import time
from typing import Optional

import httpx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


async def wait_for_server(url: str, timeout: int = 30) -> bool:
    """
    Wait for the server to be ready.
    
    Args:
        url: URL to check
        timeout: Timeout in seconds
        
    Returns:
        bool: True if the server is ready, False otherwise
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code == 200:
                    return True
        except httpx.RequestError:
            pass
        
        logger.info(f"Waiting for server to be ready at {url}...")
        await asyncio.sleep(1)
    
    return False


async def run_test_script() -> None:
    """
    Run the test script to verify the seed data and resource implementation.
    """
    logger.info("Running test script")
    
    # Import and run the test script
    from app.tests.test_seed_data import test_seed_data
    await test_seed_data()


async def main() -> None:
    """
    Main function.
    """
    logger.info("Starting application and testing seed data")
    
    # Set the DATABASE_URL environment variable to use the Docker PostgreSQL container
    os.environ["DATABASE_URL"] = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
    
    # Start the application in the background
    process = subprocess.Popen(
        ["python", "run.py"],
        cwd="backend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=os.environ.copy()  # Pass the modified environment variables
    )
    
    logger.info(f"Started application with PID {process.pid}")
    
    try:
        # Wait for the server to be ready
        server_ready = await wait_for_server("http://localhost:8000/health")
        if not server_ready:
            logger.error("Server failed to start within the timeout period")
            return
        
        logger.info("Server is ready")
        
        # Run the test script
        await run_test_script()
        
    finally:
        # Shut down the application
        logger.info("Shutting down application")
        if process.poll() is None:  # If process is still running
            os.kill(process.pid, signal.SIGTERM)
            process.wait()
        
        # Print any output from the application
        stdout, stderr = process.communicate()
        if stdout:
            logger.info(f"Application stdout:\n{stdout}")
        if stderr:
            logger.error(f"Application stderr:\n{stderr}")


if __name__ == "__main__":
    asyncio.run(main())
