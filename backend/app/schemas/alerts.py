"""
Pydantic models for the Alerts (告警通知) API.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AlertResponse(BaseModel):
    """Alert item in a list response."""
    alert_id: str
    related_event_id: Optional[str] = None
    alert_type: str
    severity: str
    title: str
    message: Optional[str] = None
    status: str
    created_time: Optional[str] = None


class UnreadCountResponse(BaseModel):
    """Unread alert count."""
    count: int


class BatchAcknowledgeRequest(BaseModel):
    """Batch acknowledge request body."""
    alert_ids: list[str]
