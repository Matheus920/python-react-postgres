import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, field_validator, AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # CORS configuration
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Database configuration
    DATABASE_URI: str = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"

    # Project information
    PROJECT_NAME: str = "Resource Management System"

    # Cache configuration
    CACHE_ENABLED: bool = True
    CACHE_EXPIRE_SECONDS: int = 60 * 5  # 5 minutes

    model_config = {
        "case_sensitive": True,
        "env_file": ".env",
        "extra": "ignore"  # Allow extra fields from environment variables
    }


settings = Settings()
