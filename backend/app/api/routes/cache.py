from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_current_admin_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import Message
from app.utils.caching import get_cache_stats, clear_expired_cache, invalidate_cache

router = APIRouter(prefix="/cache", tags=["cache"])


@router.get("/stats", response_model=Dict[str, Any])
async def read_cache_stats(
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    Get cache statistics.
    
    Only admin users can access this endpoint.
    """
    return get_cache_stats()


@router.post("/clear-expired", response_model=Message)
async def clear_expired_cache_entries(
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    Clear expired cache entries.
    
    Only admin users can access this endpoint.
    """
    cleared_count = clear_expired_cache()
    return {"message": f"Cleared {cleared_count} expired cache entries"}


@router.post("/invalidate", response_model=Message)
async def invalidate_cache_entries(
    prefix: str = None,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    Invalidate cache entries.
    
    Args:
        prefix: Optional prefix to filter cache keys
        
    Only superusers can access this endpoint.
    """
    invalidate_cache(prefix)
    if prefix:
        return {"message": f"Invalidated cache entries with prefix '{prefix}'"}
    else:
        return {"message": "Invalidated all cache entries"}
