"""
Pydantic models for Authentication API.
"""

from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Login request body."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Login success response."""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str
    display_name: str
    role: str


class UserResponse(BaseModel):
    """User info response."""
    user_id: str
    username: str
    display_name: str
    role: str
    is_active: bool
    created_time: Optional[str] = None


class SeedUserItem(BaseModel):
    """Seed user definition."""
    username: str
    password: str
    display_name: str
    role: str
