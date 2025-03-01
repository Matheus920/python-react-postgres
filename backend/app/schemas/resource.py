from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator, ConfigDict
import json


# Shared properties
class ResourceBase(BaseModel):
    """
    Base resource schema with shared properties.
    """
    name: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    meta_data: Optional[str] = None  # Renamed from metadata to match the model
    is_public: Optional[bool] = False
    
    model_config = ConfigDict(arbitrary_types_allowed=True)


# Properties to receive via API on creation
class ResourceCreate(ResourceBase):
    """
    Schema for creating a new resource.
    """
    name: str
    
    @validator("meta_data")
    def validate_metadata(cls, v):
        """Validate that metadata is valid JSON if provided."""
        if v:
            try:
                json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("Metadata must be valid JSON")
        return v


# Properties to receive via API on update
class ResourceUpdate(ResourceBase):
    """
    Schema for updating a resource.
    """
    pass


# Properties to return via API
class Resource(ResourceBase):
    """
    Schema for returning a resource.
    """
    id: int
    name: str
    owner_id: int
    
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
    
    @property
    def metadata_dict(self) -> Dict[str, Any]:
        """
        Get metadata as a dictionary.
        
        Returns:
            Dict[str, Any]: Metadata as a dictionary
        """
        if self.meta_data:
            try:
                return json.loads(self.meta_data)
            except json.JSONDecodeError:
                return {}
        return {}


# Properties to return via API for a list of resources
class ResourceList(BaseModel):
    """
    Schema for returning a list of resources.
    """
    resources: List[Resource]
    total: int
    
    model_config = ConfigDict(arbitrary_types_allowed=True)


# Schema for resource sharing
class ResourceShare(BaseModel):
    """
    Schema for sharing a resource with a user.
    """
    user_id: int
    permission_type: str = Field(..., description="Permission type (read, write, admin)")
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
