from typing import List, Optional, Dict, Any, Union

from sqlalchemy import select, and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.resource import Resource, resource_permission
from app.repositories.base import BaseRepository
from app.schemas.resource import ResourceCreate, ResourceUpdate
from app.utils.caching import cached, invalidate_cache


class ResourceRepository(BaseRepository[Resource, ResourceCreate, ResourceUpdate]):
    """
    Repository for Resource model.
    """
    
    @cached()
    async def get_by_user(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Resource]:
        """
        Get resources owned by or shared with a user.
        
        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Resource]: List of resources
        """
        query = (
            select(Resource)
            .where(
                or_(
                    Resource.owner_id == user_id,
                    Resource.id.in_(
                        select(resource_permission.c.resource_id)
                        .where(resource_permission.c.user_id == user_id)
                    )
                )
            )
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    @cached()
    async def count_by_user(self, db: AsyncSession, *, user_id: int) -> int:
        """
        Count resources owned by or shared with a user.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            int: Number of resources
        """
        query = select(func.count()).where(
            or_(
                Resource.owner_id == user_id,
                Resource.id.in_(
                    select(resource_permission.c.resource_id)
                    .where(resource_permission.c.user_id == user_id)
                )
            )
        )
        result = await db.execute(query)
        return result.scalar_one()
    
    @cached()
    async def get_by_owner(
        self, 
        db: AsyncSession, 
        *, 
        owner_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Resource]:
        """
        Get resources owned by a user.
        
        Args:
            db: Database session
            owner_id: Owner ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Resource]: List of resources
        """
        query = (
            select(Resource)
            .where(Resource.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()
    
    @cached()
    async def count_by_owner(self, db: AsyncSession, *, owner_id: int) -> int:
        """
        Count resources owned by a user.
        
        Args:
            db: Database session
            owner_id: Owner ID
            
        Returns:
            int: Number of resources
        """
        query = select(func.count()).where(Resource.owner_id == owner_id)
        result = await db.execute(query)
        return result.scalar_one()
    
    @cached()
    async def get_with_filter(
        self,
        db: AsyncSession,
        *,
        owner_id: Optional[int] = None,
        is_public: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = "asc",
        skip: int = 0,
        limit: int = 100
    ) -> List[Resource]:
        """
        Get resources with filtering and sorting.
        
        Args:
            db: Database session
            owner_id: Optional owner ID filter
            is_public: Optional public status filter
            search: Optional search term for name or description
            sort_by: Optional field to sort by (name, created_at, etc.)
            sort_order: Optional sort order (asc or desc)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Resource]: List of resources
        """
        query = select(Resource)
        
        # Apply filters
        filters = []
        if owner_id is not None:
            filters.append(Resource.owner_id == owner_id)
        if is_public is not None:
            filters.append(Resource.is_public == is_public)
        if search:
            filters.append(
                or_(
                    Resource.name.ilike(f"%{search}%"),
                    Resource.description.ilike(f"%{search}%")
                )
            )
        
        if filters:
            query = query.where(and_(*filters))
        
        # Apply sorting
        if sort_by:
            column = getattr(Resource, sort_by, None)
            if column is not None:
                if sort_order.lower() == "desc":
                    query = query.order_by(column.desc())
                else:
                    query = query.order_by(column.asc())
            else:
                # Default sort by id if column not found
                query = query.order_by(Resource.id.asc())
        else:
            # Default sort by id
            query = query.order_by(Resource.id.asc())
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    @cached()
    async def count_with_filter(
        self,
        db: AsyncSession,
        *,
        owner_id: Optional[int] = None,
        is_public: Optional[bool] = None,
        search: Optional[str] = None
    ) -> int:
        """
        Count resources with filtering.
        
        Args:
            db: Database session
            owner_id: Optional owner ID filter
            is_public: Optional public status filter
            search: Optional search term for name or description
            
        Returns:
            int: Number of resources
        """
        query = select(func.count()).select_from(Resource)
        
        # Apply filters
        filters = []
        if owner_id is not None:
            filters.append(Resource.owner_id == owner_id)
        if is_public is not None:
            filters.append(Resource.is_public == is_public)
        if search:
            filters.append(
                or_(
                    Resource.name.ilike(f"%{search}%"),
                    Resource.description.ilike(f"%{search}%")
                )
            )
        
        if filters:
            query = query.where(and_(*filters))
        
        result = await db.execute(query)
        return result.scalar_one()
    
    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: ResourceCreate, owner_id: int
    ) -> Resource:
        """
        Create a new resource with owner.
        
        Args:
            db: Database session
            obj_in: Resource creation schema
            owner_id: Owner ID
            
        Returns:
            Resource: Created resource
        """
        obj_in_data = obj_in.dict()
        db_obj = Resource(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        
        # Invalidate cache
        invalidate_cache("ResourceRepository")
        
        return db_obj
    
    async def update_with_owner_check(
        self,
        db: AsyncSession,
        *,
        db_obj: Resource,
        obj_in: Union[ResourceUpdate, Dict[str, Any]],
        current_user_id: int
    ) -> Resource:
        """
        Update a resource with owner check.
        
        Args:
            db: Database session
            db_obj: Resource to update
            obj_in: Resource update schema or dictionary
            current_user_id: Current user ID
            
        Returns:
            Resource: Updated resource
            
        Raises:
            ValueError: If the current user is not the owner
        """
        if db_obj.owner_id != current_user_id:
            raise ValueError("Not enough permissions")
        
        resource = await super().update(db, db_obj=db_obj, obj_in=obj_in)
        
        # Invalidate cache
        invalidate_cache("ResourceRepository")
        
        return resource
    
    async def remove_with_owner_check(
        self, db: AsyncSession, *, id: int, current_user_id: int
    ) -> Resource:
        """
        Remove a resource with owner check.
        
        Args:
            db: Database session
            id: Resource ID
            current_user_id: Current user ID
            
        Returns:
            Resource: Removed resource
            
        Raises:
            ValueError: If the current user is not the owner
        """
        resource = await self.get(db=db, id=id)
        if not resource:
            raise ValueError("Resource not found")
        
        if resource.owner_id != current_user_id:
            raise ValueError("Not enough permissions")
        
        await db.delete(resource)
        await db.commit()
        
        # Invalidate cache
        invalidate_cache("ResourceRepository")
        
        return resource
    
    async def share_resource(
        self, db: AsyncSession, *, resource_id: int, user_id: int, permission_type: str
    ) -> None:
        """
        Share a resource with a user.
        
        Args:
            db: Database session
            resource_id: Resource ID
            user_id: User ID
            permission_type: Permission type
        """
        # Check if the resource exists
        resource = await self.get(db=db, id=resource_id)
        if not resource:
            raise ValueError("Resource not found")
        
        # Add the permission
        stmt = resource_permission.insert().values(
            resource_id=resource_id,
            user_id=user_id,
            permission_type=permission_type
        )
        await db.execute(stmt)
        await db.commit()
        
        # Invalidate cache
        invalidate_cache("ResourceRepository")
    
    async def unshare_resource(
        self, db: AsyncSession, *, resource_id: int, user_id: int
    ) -> None:
        """
        Unshare a resource from a user.
        
        Args:
            db: Database session
            resource_id: Resource ID
            user_id: User ID
        """
        # Check if the resource exists
        resource = await self.get(db=db, id=resource_id)
        if not resource:
            raise ValueError("Resource not found")
        
        # Remove the permission
        stmt = resource_permission.delete().where(
            and_(
                resource_permission.c.resource_id == resource_id,
                resource_permission.c.user_id == user_id
            )
        )
        await db.execute(stmt)
        await db.commit()
        
        # Invalidate cache
        invalidate_cache("ResourceRepository")


# Create a singleton instance
resource_repository = ResourceRepository(Resource)
