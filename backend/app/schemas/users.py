"""
Pydantic models for User Management API.
"""

from typing import Optional

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    """Create user request body."""
    username: str
    password: str
    display_name: str
    role: str = "viewer"


class UpdateUserRequest(BaseModel):
    """Update user request body (all optional)."""
    username: Optional[str] = None
    password: Optional[str] = None
    display_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
