from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import Message
from app.schemas.resource import (
    Resource as ResourceSchema,
    ResourceCreate,
    ResourceUpdate,
    ResourceShare,
)
from app.services.resource import resource_service
from app.utils.pagination import PaginationParams, Page

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("/", response_model=Page[ResourceSchema])
async def read_resources(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    owner_id: Optional[int] = None,
    is_public: Optional[bool] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = Query(None, description="Field to sort by (name, id, etc.)"),
    sort_order: Optional[str] = Query("asc", description="Sort order (asc or desc)"),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve resources with filtering, sorting, and pagination.
    """
    return await resource_service.get_resources(
        db=db,
        pagination=pagination,
        current_user=current_user,
        owner_id=owner_id,
        is_public=is_public,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/me", response_model=Page[ResourceSchema])
async def read_my_resources(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    sort_by: Optional[str] = Query(None, description="Field to sort by (name, id, etc.)"),
    sort_order: Optional[str] = Query("asc", description="Sort order (asc or desc)"),
    is_public: Optional[bool] = Query(None, description="Filter by public status"),
    search: Optional[str] = Query(None, description="Search term for name or description"),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve resources owned by or shared with the current user.
    """
    return await resource_service.get_user_resources(
        db=db,
        pagination=pagination,
        user_id=current_user.id,
        sort_by=sort_by,
        sort_order=sort_order,
        is_public=is_public,
        search=search,
    )


@router.post("/", response_model=ResourceSchema)
async def create_resource(
    *,
    db: AsyncSession = Depends(get_db),
    resource_in: ResourceCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new resource.
    """
    return await resource_service.create_resource(
        db=db, obj_in=resource_in, current_user=current_user
    )


@router.get("/{id}", response_model=ResourceSchema)
async def read_resource(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get resource by ID.
    """
    resource = await resource_service.get_resource(
        db=db, id=id, current_user=current_user
    )
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )
    return resource


@router.put("/{id}", response_model=ResourceSchema)
async def update_resource(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    resource_in: ResourceUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a resource.
    """
    return await resource_service.update_resource(
        db=db, id=id, obj_in=resource_in, current_user=current_user
    )


@router.delete("/{id}", response_model=ResourceSchema)
async def delete_resource(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a resource.
    """
    return await resource_service.delete_resource(
        db=db, id=id, current_user=current_user
    )


@router.post("/{id}/share", response_model=Message)
async def share_resource(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    share_data: ResourceShare,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Share a resource with a user.
    """
    await resource_service.share_resource(
        db=db, id=id, share_data=share_data, current_user=current_user
    )
    return {"message": "Resource shared successfully"}


@router.delete("/{id}/share/{user_id}", response_model=Message)
async def unshare_resource(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    user_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Unshare a resource from a user.
    """
    await resource_service.unshare_resource(
        db=db, id=id, user_id=user_id, current_user=current_user
    )
    return {"message": "Resource unshared successfully"}
