"""
Pydantic models for the Inference Tasks (推理任务) API.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    """Request body for creating an inference task."""
    video_id: str
    model_id: str
    task_name: Optional[str] = None


class TaskQueryParams(BaseModel):
    """Query parameters for listing tasks."""
    page_no: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    task_status: Optional[str] = None
    video_id: Optional[str] = None


class TaskResponse(BaseModel):
    """Inference task item."""
    task_id: str
    video_id: str
    model_id: str
    task_name: str
    task_status: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    result_summary: Optional[str] = None
    error_message: Optional[str] = None
    created_time: Optional[str] = None
