from typing import Any, Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

# Define a model config that allows arbitrary types
model_config = ConfigDict(arbitrary_types_allowed=True)


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


class Message(BaseModel):
    """
    Generic message response.
    
    Attributes:
        message: Message text
    """
    message: str


class ErrorResponse(BaseModel):
    """
    Error response.
    
    Attributes:
        detail: Error detail
    """
    detail: str


class SuccessResponse(BaseModel):
    """
    Success response.
    
    Attributes:
        success: Whether the operation was successful
        message: Success message
        data: Optional data
    """
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None
