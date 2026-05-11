"""
Pydantic models for the Events (事件中心) API.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EventQueryParams(BaseModel):
    """Query parameters for listing events."""
    page_no: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    object_type: Optional[str] = None
    object_id: Optional[str] = None
    event_type: Optional[str] = None
    risk_level: Optional[str] = None
    scene_type: Optional[str] = None
    review_status: Optional[str] = None
    video_name: Optional[str] = None


class EventResponse(BaseModel):
    """Event item in a list response."""
    event_id: str
    object_id: str
    object_name: Optional[str] = None
    video_id: str
    video_name: Optional[str] = None
    event_type: str
    risk_level: str
    scene_type: Optional[str] = None
    event_time: Optional[str] = None
    start_second: int
    end_second: int
    thumbnail_url: Optional[str] = None
    result_desc: Optional[str] = None
    review_status: str
    review_remark: Optional[str] = None


class EventDetailResponse(EventResponse):
    """Full event detail including extra fields."""
    clip_url: Optional[str] = None
    created_time: Optional[str] = None
    updated_time: Optional[str] = None


class EventReviewRequest(BaseModel):
    """Request body for reviewing an event."""
    review_status: str = Field(..., pattern=r"^(pending|reviewed)$")
    review_remark: Optional[str] = None


class EventReviewResponse(BaseModel):
    """Response after reviewing an event."""
    event_id: str
    review_status: str
    review_remark: Optional[str] = None
