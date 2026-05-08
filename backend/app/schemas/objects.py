"""
Pydantic models for the Objects (监测对象) API.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ObjectQueryParams(BaseModel):
    """Query parameters for listing objects."""
    object_type: Optional[str] = None  # bridge / tunnel
    status: Optional[str] = None      # active / inactive


class ObjectResponse(BaseModel):
    """Single object response."""
    object_id: str
    object_name: str
    object_type: str
    location_desc: Optional[str] = None
    status: str


# ObjectListResponse is returned as a plain list via success_response()
