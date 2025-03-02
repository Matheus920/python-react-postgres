from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.routes import auth, users, resources, cache
from app.core.config import settings
from app.core.middleware import CacheCleanupMiddleware
from app.db.seed import seed_db

# Configure logging
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Resource Management System API",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # Disable automatic redirection of trailing slashes to avoid authentication issues
    redirect_slashes=False,
)

# Set up middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add cache cleanup middleware
app.add_middleware(
    CacheCleanupMiddleware,
    cleanup_interval=settings.CACHE_EXPIRE_SECONDS // 2,  # Clean up at half the cache expiration time
)

# Include API routes
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(resources.router, prefix=settings.API_V1_STR)
app.include_router(cache.router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    """
    Initialize application on startup.
    """
    logger.info("Starting up application")
    
    # Seed the database with initial data
    # Use force=False to avoid cleaning the database before seeding
    await seed_db(force=False)


@app.get("/")
async def root():
    return {"message": "Welcome to the Resource Management System API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
