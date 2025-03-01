from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_current_admin_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate
from app.services.user import user_service
from app.utils.pagination import PaginationParams, Page

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=Page[UserSchema])
async def read_users(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    Retrieve users.
    
    Only admin users can access this endpoint.
    """
    return await user_service.get_users(db=db, pagination=pagination)


@router.post("/", response_model=UserSchema)
async def create_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    """
    Create new user.
    
    Only admin users can access this endpoint.
    """
    return await user_service.create_user(db=db, obj_in=user_in)


@router.get("/me", response_model=UserSchema)
async def read_user_me(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return await user_service.get_me(db=db, current_user=current_user)


@router.put("/me", response_model=UserSchema)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update current user.
    """
    return await user_service.update_user(
        db=db, user_id=current_user.id, obj_in=user_in, current_user=current_user
    )


@router.get("/{user_id}", response_model=UserSchema)
async def read_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get user by ID.
    
    Regular users can only access their own user.
    Admin users can access any user.
    """
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return await user_service.get_user(db=db, user_id=user_id)


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a user.
    
    Regular users can only update their own user.
    Admin users can update any user.
    """
    return await user_service.update_user(
        db=db, user_id=user_id, obj_in=user_in, current_user=current_user
    )


@router.delete("/{user_id}", response_model=UserSchema)
async def delete_user(
    *,
    db: AsyncSession = Depends(get_db),
    user_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a user.
    
    Regular users can only delete their own user.
    Admin users can delete any user.
    """
    return await user_service.delete_user(
        db=db, user_id=user_id, current_user=current_user
    )
