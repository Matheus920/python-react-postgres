from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """
    Schema for JWT token.
    
    Attributes:
        access_token: JWT access token
        token_type: Token type (always "bearer")
    """
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Schema for JWT token payload.
    
    Attributes:
        sub: Subject (user ID)
        exp: Expiration time
    """
    sub: Optional[str] = None
    exp: Optional[int] = None


class Login(BaseModel):
    """
    Schema for login credentials.
    
    Attributes:
        username: Username or email
        password: Password
    """
    username: str
    password: str


class PasswordReset(BaseModel):
    """
    Schema for password reset.
    
    Attributes:
        token: Password reset token
        new_password: New password
    """
    token: str
    new_password: str


class PasswordResetRequest(BaseModel):
    """
    Schema for password reset request.
    
    Attributes:
        email: Email address
    """
    email: str
