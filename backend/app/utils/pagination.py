from typing import Any, Dict, Generic, List, Optional, TypeVar

from fastapi import Query
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

# Define a model config that allows arbitrary types
model_config = ConfigDict(arbitrary_types_allowed=True)


class PaginationParams:
    """
    Pagination parameters for API endpoints.
    
    Attributes:
        skip: Number of records to skip
        limit: Maximum number of records to return
    """

    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    ):
        self.skip = skip
        self.limit = limit


class PageInfo(BaseModel):
    """
    Pagination information.
    
    Attributes:
        total: Total number of records
        page: Current page number
        pages: Total number of pages
        has_next: Whether there is a next page
        has_prev: Whether there is a previous page
    """

    total: int
    page: int
    pages: int
    has_next: bool
    has_prev: bool


class Page(BaseModel, Generic[T]):
    """
    Paginated response.
    
    Attributes:
        items: List of items
        page_info: Pagination information
    """

    items: List[T]
    page_info: PageInfo
    
    model_config = model_config


def create_page_info(
    total: int, page_params: PaginationParams, page: Optional[int] = None
) -> PageInfo:
    """
    Create pagination information.
    
    Args:
        total: Total number of records
        page_params: Pagination parameters
        page: Current page number (calculated from skip and limit if not provided)
        
    Returns:
        PageInfo: Pagination information
    """
    if page is None:
        page = (page_params.skip // page_params.limit) + 1 if page_params.limit else 1

    pages = (total // page_params.limit) + (1 if total % page_params.limit else 0) if page_params.limit else 1
    
    return PageInfo(
        total=total,
        page=page,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1,
    )


def create_page(
    items: List[T], total: int, page_params: PaginationParams, page: Optional[int] = None
) -> Page[T]:
    """
    Create a paginated response.
    
    Args:
        items: List of items
        total: Total number of records
        page_params: Pagination parameters
        page: Current page number (calculated from skip and limit if not provided)
        
    Returns:
        Page[T]: Paginated response
    """
    page_info = create_page_info(total, page_params, page)
    return Page(items=items, page_info=page_info)
