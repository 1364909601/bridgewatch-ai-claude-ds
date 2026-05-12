"""
Pydantic models for Monitoring Data API.
"""

from typing import Optional

from pydantic import BaseModel


class MonitoringPoint(BaseModel):
    """Single monitoring data point."""
    data_id: int
    object_id: str
    data_type: str
    data_value: float
    data_time: str
    ext_json: Optional[dict] = None
