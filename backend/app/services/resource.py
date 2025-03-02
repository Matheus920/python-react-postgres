from typing import List, Optional, Dict, Any

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resource import Resource
from app.models.user import User
from app.repositories.resource import resource_repository
from app.schemas.resource import ResourceCreate, ResourceUpdate, ResourceShare
from app.utils.caching import cached
from app.utils.pagination import PaginationParams, create_page, Page


class ResourceService:
    """
    Service for resource operations.
    """
    
    async def get_resource(
        self,
        db: AsyncSession,
        *,
        id: int,
        current_user: User
    ) -> Optional[Resource]:
        """
        Get a resource by ID.
        
        Args:
            db: Database session
            id: Resource ID
            current_user: Current user
            
        Returns:
            Optional[Resource]: Resource if found and accessible, None otherwise
            
        Raises:
            HTTPException: If the resource is not found or not accessible
        """
        resource = await resource_repository.get(db, id=id)
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found",
            )
        
        # Admin users can access any resource
        if current_user.is_admin:
            return resource
        
        # Check if the user has access to the resource
        if resource.owner_id != current_user.id and not resource.is_public:
            # Check if the resource is shared with the user
            if not resource.has_permission(current_user.id, "read"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions",
                )
        
        return resource
    
    @cached()
    async def get_resources(
        self,
        db: AsyncSession,
        *,
        pagination: PaginationParams,
        current_user: User,
        owner_id: Optional[int] = None,
        is_public: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc"
    ) -> Page[Resource]:
        """
        Get resources with pagination, filtering, and sorting.
        
        Args:
            db: Database session
            pagination: Pagination parameters
            current_user: Current user
            owner_id: Optional owner ID filter
            is_public: Optional public status filter
            search: Optional search term
            sort_by: Optional field to sort by
            sort_order: Optional sort order (asc or desc)
            
        Returns:
            Page[Resource]: Paginated resources
        """
        # If user is admin, they can see all resources with applied filters
        # If user is not admin, they can only see their own resources or resources shared with them
        if current_user.is_admin:
            # Admin user - get resources with filters
            resources = await resource_repository.get_with_filter(
                db,
                owner_id=owner_id,
                is_public=is_public,
                search=search,
                sort_by=sort_by,
                sort_order=sort_order,
                skip=pagination.skip,
                limit=pagination.limit
            )
            
            # Count total resources
            total = await resource_repository.count_with_filter(
                db,
                owner_id=owner_id,
                is_public=is_public,
                search=search
            )
        else:
            # Regular user - get only resources they own or have been shared with them
            # If owner_id is specified and it's not the current user, ignore it for security
            effective_owner_id = owner_id if owner_id == current_user.id else None
            
            if effective_owner_id is None:
                # Get resources owned by or shared with the user
                resources = await resource_repository.get_by_user(
                    db,
                    user_id=current_user.id,
                    skip=pagination.skip,
                    limit=pagination.limit,
                    sort_by=sort_by,
                    sort_order=sort_order,
                    is_public=is_public,
                    search=search
                )
                
                # Count total resources
                total = await resource_repository.count_by_user(
                    db, 
                    user_id=current_user.id,
                    is_public=is_public,
                    search=search
                )
            else:
                # Get only resources owned by the user (with additional filters)
                resources = await resource_repository.get_with_filter(
                    db,
                    owner_id=current_user.id,
                    is_public=is_public,
                    search=search,
                    sort_by=sort_by,
                    sort_order=sort_order,
                    skip=pagination.skip,
                    limit=pagination.limit
                )
                
                # Count total resources
                total = await resource_repository.count_with_filter(
                    db,
                    owner_id=current_user.id,
                    is_public=is_public,
                    search=search
                )
        
        # Create paginated response
        return create_page(resources, total, pagination)
    
    @cached()
    async def get_user_resources(
        self,
        db: AsyncSession,
        *,
        pagination: PaginationParams,
        user_id: int,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        is_public: Optional[bool] = None,
        search: Optional[str] = None
    ) -> Page[Resource]:
        """
        Get resources owned by or shared with a user.
        
        Args:
            db: Database session
            pagination: Pagination parameters
            user_id: User ID
            sort_by: Optional field to sort by
            sort_order: Optional sort order (asc or desc)
            is_public: Optional public status filter
            search: Optional search term
            
        Returns:
            Page[Resource]: Paginated resources
        """
        # Get resources
        resources = await resource_repository.get_by_user(
            db,
            user_id=user_id,
            skip=pagination.skip,
            limit=pagination.limit,
            sort_by=sort_by,
            sort_order=sort_order,
            is_public=is_public,
            search=search
        )
        
        # Count total resources
        total = await resource_repository.count_by_user(
            db, 
            user_id=user_id,
            is_public=is_public,
            search=search
        )
        
        # Create paginated response
        return create_page(resources, total, pagination)
    
    async def create_resource(
        self,
        db: AsyncSession,
        *,
        obj_in: ResourceCreate,
        current_user: User
    ) -> Resource:
        """
        Create a new resource.
        
        Args:
            db: Database session
            obj_in: Resource creation schema
            current_user: Current user
            
        Returns:
            Resource: Created resource
        """
        return await resource_repository.create_with_owner(
            db, obj_in=obj_in, owner_id=current_user.id
        )
    
    async def update_resource(
        self,
        db: AsyncSession,
        *,
        id: int,
        obj_in: ResourceUpdate,
        current_user: User
    ) -> Resource:
        """
        Update a resource.
        
        Args:
            db: Database session
            id: Resource ID
            obj_in: Resource update schema
            current_user: Current user
            
        Returns:
            Resource: Updated resource
            
        Raises:
            HTTPException: If the resource is not found or the user is not the owner
        """
        resource = await resource_repository.get(db, id=id)
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found",
            )
        
        # Admin users can update any resource
        if current_user.is_admin:
            return await resource_repository.update(db, db_obj=resource, obj_in=obj_in)
        
        try:
            return await resource_repository.update_with_owner_check(
                db, db_obj=resource, obj_in=obj_in, current_user_id=current_user.id
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e),
            )
    
    async def delete_resource(
        self,
        db: AsyncSession,
        *,
        id: int,
        current_user: User
    ) -> Resource:
        """
        Delete a resource.
        
        Args:
            db: Database session
            id: Resource ID
            current_user: Current user
            
        Returns:
            Resource: Deleted resource
            
        Raises:
            HTTPException: If the resource is not found or the user is not the owner
        """
        # Admin users can delete any resource
        if current_user.is_admin:
            resource = await resource_repository.get(db, id=id)
            if not resource:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Resource not found",
                )
            return await resource_repository.remove(db, id=id)
        
        try:
            return await resource_repository.remove_with_owner_check(
                db, id=id, current_user_id=current_user.id
            )
        except ValueError as e:
            if "not found" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=str(e),
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=str(e),
                )
    
    async def share_resource(
        self,
        db: AsyncSession,
        *,
        id: int,
        share_data: ResourceShare,
        current_user: User
    ) -> None:
        """
        Share a resource with a user.
        
        Args:
            db: Database session
            id: Resource ID
            share_data: Resource sharing data
            current_user: Current user
            
        Raises:
            HTTPException: If the resource is not found or the user is not the owner
        """
        resource = await resource_repository.get(db, id=id)
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found",
            )
        
        # Admin users can share any resource
        if not current_user.is_admin and resource.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        
        try:
            await resource_repository.share_resource(
                db,
                resource_id=id,
                user_id=share_data.user_id,
                permission_type=share_data.permission_type
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
    
    async def unshare_resource(
        self,
        db: AsyncSession,
        *,
        id: int,
        user_id: int,
        current_user: User
    ) -> None:
        """
        Unshare a resource from a user.
        
        Args:
            db: Database session
            id: Resource ID
            user_id: User ID
            current_user: Current user
            
        Raises:
            HTTPException: If the resource is not found or the user is not the owner
        """
        resource = await resource_repository.get(db, id=id)
        if not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found",
            )
        
        # Admin users can unshare any resource
        if not current_user.is_admin and resource.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        
        try:
            await resource_repository.unshare_resource(
                db, resource_id=id, user_id=user_id
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )


# Create a singleton instance
resource_service = ResourceService()
