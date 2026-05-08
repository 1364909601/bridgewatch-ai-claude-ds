"""
Service layer for Dicts (数据字典).
"""

from fastapi import HTTPException


# Static dictionary data (no DB table yet — can be moved to DB later)
_DICT_DATA = {
    "object_type": [
        {"value": "bridge", "label": "桥梁"},
        {"value": "tunnel", "label": "隧道"},
    ],
    "scene_type": [
        {"value": "day", "label": "白天"},
        {"value": "night", "label": "夜间"},
        {"value": "rain_fog", "label": "雨雾"},
    ],
    "risk_level": [
        {"value": "low", "label": "低风险"},
        {"value": "medium", "label": "中风险"},
        {"value": "high", "label": "高风险"},
    ],
    "review_status": [
        {"value": "pending", "label": "待复核"},
        {"value": "reviewed", "label": "已确认"},
    ],
    "event_type": [
        {"value": "collapse", "label": "桥梁坍塌"},
        {"value": "deformation", "label": "桥面大变形"},
        {"value": "congestion", "label": "车辆积压"},
        {"value": "fire", "label": "桥面火灾"},
        {"value": "ship_collision", "label": "船舶碰撞"},
    ],
    "task_status": [
        {"value": "queued", "label": "排队中"},
        {"value": "running", "label": "运行中"},
        {"value": "success", "label": "已完成"},
        {"value": "failed", "label": "失败"},
    ],
    "model_status": [
        {"value": "active", "label": "启用"},
        {"value": "inactive", "label": "停用"},
        {"value": "deprecated", "label": "废弃"},
    ],
}


class DictService:
    """Business logic for dictionary data."""

    @staticmethod
    def get_dict(dict_type: str) -> list[dict]:
        """Get dictionary items by type."""
        if dict_type not in _DICT_DATA:
            raise HTTPException(status_code=404, detail=f"字典类型 '{dict_type}' 不存在")
        return _DICT_DATA[dict_type]
