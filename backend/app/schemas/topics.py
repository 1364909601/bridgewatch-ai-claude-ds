"""
Pydantic models for the Topics (专题分析) API.
"""

from typing import Optional

from pydantic import BaseModel


class EventTypeStat(BaseModel):
    """Event type statistics."""
    event_type: str
    event_type_name: str
    count: int


class SceneStat(BaseModel):
    """Scene statistics."""
    scene_type: str
    count: int


class BridgeSummaryResponse(BaseModel):
    """Bridge topic summary."""
    event_type_stats: list[EventTypeStat]
    scene_stats: list[SceneStat]


class FusionResultResponse(BaseModel):
    """Ship collision fusion result."""
    fusion_id: str
    score: Optional[float] = None
    risk_level: str
    rule_desc: Optional[str] = None
    fusion_time: Optional[str] = None
    related_event_id: Optional[str] = None
