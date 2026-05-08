"""
Pydantic models for the Dashboard (总览面板) API.
"""

from typing import Optional

from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    """Dashboard summary statistics."""
    total: int
    high_risk: int
    bridges: int
    tunnels: int


class DashboardTrendPoint(BaseModel):
    """Single day trend data point."""
    date: str
    count: int
    high_risk: int


class DashboardDistributionItem(BaseModel):
    """Event type distribution item."""
    event_type: str
    event_type_name: str
    count: int
