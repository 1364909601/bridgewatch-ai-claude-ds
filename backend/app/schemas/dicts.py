"""
Pydantic models for the Dicts (数据字典) API.
"""

from pydantic import BaseModel


class DictItem(BaseModel):
    """Dictionary item with value-label pair."""
    value: str
    label: str
