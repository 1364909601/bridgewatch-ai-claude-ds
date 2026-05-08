"""
Pydantic models for the Videos (视频管理) API.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class VideoQueryParams(BaseModel):
    """Query parameters for listing videos."""
    page_no: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    object_id: Optional[str] = None
    scene_type: Optional[str] = None


class VideoResponse(BaseModel):
    """Video item in a list response."""
    video_id: str
    object_id: str
    video_name: str
    file_url: str
    capture_time: Optional[str] = None
    duration_seconds: int
    resolution: Optional[str] = None
    scene_type: Optional[str] = None
    preprocess_status: str


class VideoEventMarkResponse(BaseModel):
    """Event mark on a video timeline."""
    event_id: str
    event_type: str
    risk_level: str
    start_second: int
    end_second: int


class VideoPlayUrlResponse(BaseModel):
    """Video play URL response."""
    video_id: str
    play_url: str
    duration_seconds: int
