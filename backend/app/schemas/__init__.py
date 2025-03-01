from app.schemas.user import User, UserCreate, UserUpdate, UserInDB, UserList
from app.schemas.auth import Token, TokenPayload, Login, PasswordReset, PasswordResetRequest
from app.schemas.resource import Resource, ResourceCreate, ResourceUpdate, ResourceList, ResourceShare
from app.schemas.common import Page, PageInfo, Message, ErrorResponse, SuccessResponse

# For easy imports
__all__ = [
    "User", "UserCreate", "UserUpdate", "UserInDB", "UserList",
    "Token", "TokenPayload", "Login", "PasswordReset", "PasswordResetRequest",
    "Resource", "ResourceCreate", "ResourceUpdate", "ResourceList", "ResourceShare",
    "Page", "PageInfo", "Message", "ErrorResponse", "SuccessResponse",
]
