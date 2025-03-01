import functools
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db

# Configure logging
logger = logging.getLogger(__name__)

# Simple in-memory cache
_cache: Dict[str, Dict[str, Any]] = {}

T = TypeVar("T")


def _get_cache_key(func: Callable, *args: Any, **kwargs: Any) -> str:
    """
    Generate a cache key based on function name and arguments.
    
    Args:
        func: Function to cache
        args: Positional arguments
        kwargs: Keyword arguments
        
    Returns:
        str: Cache key
    """
    # Convert args and kwargs to a string representation
    key_parts = [func.__module__, func.__name__]
    
    # Add args to key parts
    for arg in args:
        if isinstance(arg, (str, int, float, bool, type(None))):
            key_parts.append(str(arg))
        elif hasattr(arg, "__dict__"):
            # For objects, use their __dict__ representation
            key_parts.append(str(arg.__dict__))
        else:
            # For other types, use their string representation
            key_parts.append(str(arg))
    
    # Add kwargs to key parts
    for k, v in sorted(kwargs.items()):
        if isinstance(v, (str, int, float, bool, type(None))):
            key_parts.append(f"{k}:{v}")
        elif hasattr(v, "__dict__"):
            # For objects, use their __dict__ representation
            key_parts.append(f"{k}:{v.__dict__}")
        else:
            # For other types, use their string representation
            key_parts.append(f"{k}:{v}")
    
    # Create a hash of the key parts
    key_str = ":".join(key_parts)
    return hashlib.md5(key_str.encode()).hexdigest()


def cached(
    expire_seconds: Optional[int] = None,
    skip_kwargs: Optional[list] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Cache decorator for functions.
    
    Args:
        expire_seconds: Cache expiration time in seconds (defaults to settings.CACHE_EXPIRE_SECONDS)
        skip_kwargs: List of keyword arguments to skip when generating cache key
        
    Returns:
        Callable: Decorated function
    """
    skip_kwargs = skip_kwargs or ["db", "request"]
    expire_time = expire_seconds or settings.CACHE_EXPIRE_SECONDS

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            if not settings.CACHE_ENABLED:
                return await func(*args, **kwargs)

            # Filter out kwargs that should be skipped
            cache_kwargs = {k: v for k, v in kwargs.items() if k not in skip_kwargs}
            
            # Generate cache key
            cache_key = _get_cache_key(func, *args, **cache_kwargs)
            
            # Check if result is in cache and not expired
            if cache_key in _cache:
                cache_item = _cache[cache_key]
                if datetime.now() < cache_item["expire_time"]:
                    return cast(T, cache_item["result"])
            
            # Call the function and cache the result
            result = await func(*args, **kwargs)
            _cache[cache_key] = {
                "result": result,
                "expire_time": datetime.now() + timedelta(seconds=expire_time),
            }
            
            return result
        
        return wrapper
    
    return decorator


def invalidate_cache(prefix: Optional[str] = None) -> None:
    """
    Invalidate cache entries.
    
    Args:
        prefix: Optional prefix to filter cache keys
    """
    global _cache
    
    if prefix:
        # Invalidate cache entries that start with the prefix
        _cache = {k: v for k, v in _cache.items() if not k.startswith(prefix)}
    else:
        # Invalidate all cache entries
        _cache = {}


def get_cache_stats() -> Dict[str, Any]:
    """
    Get cache statistics.
    
    Returns:
        Dict[str, Any]: Cache statistics
    """
    now = datetime.now()
    entries_info = []
    expired_count = 0
    active_count = 0
    
    for k, v in _cache.items():
        expires_in = (v["expire_time"] - now).total_seconds()
        is_expired = expires_in <= 0
        
        if is_expired:
            expired_count += 1
        else:
            active_count += 1
            
        entries_info.append({
            "key": k,
            "expires_in": expires_in,
            "is_expired": is_expired,
            "size": len(json.dumps(v["result"])),
        })
    
    return {
        "total_entries": len(_cache),
        "active_entries": active_count,
        "expired_entries": expired_count,
        "memory_usage": len(json.dumps(_cache)),
        "entries": entries_info,
    }


def clear_expired_cache() -> int:
    """
    Clear expired cache entries.
    
    Returns:
        int: Number of cleared entries
    """
    global _cache
    now = datetime.now()
    expired_keys = [k for k, v in _cache.items() if v["expire_time"] <= now]
    
    for k in expired_keys:
        del _cache[k]
    
    logger.info(f"Cleared {len(expired_keys)} expired cache entries")
    return len(expired_keys)
