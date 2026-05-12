"""
Service layer for Topics (专题分析).
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event_record import EventRecord
from app.models.fusion_result import FusionResult
from app.models.object_info import ObjectInfo
from app.utils.exceptions import NotFoundException


_EVENT_TYPE_LABELS = {
    "collapse": "桥梁坍塌",
    "deformation": "桥面大变形",
    "congestion": "车辆积压",
    "fire": "桥面火灾",
}


class TopicService:
    """Business logic for topic/domain-specific endpoints."""

    @staticmethod
    async def get_bridge_summary(
        db: AsyncSession,
        object_id: Optional[str] = None,
    ) -> dict:
        """Get bridge topic summary statistics."""
        query = select(
            EventRecord.event_type,
            func.count().label("count"),
        )

        if object_id:
            query = query.where(EventRecord.object_id == object_id)

        query = query.group_by(EventRecord.event_type).order_by(EventRecord.event_type)
        result = await db.execute(query)
        rows = result.all()

        return {
            "event_type_stats": [
                {
                    "event_type": r.event_type,
                    "event_type_name": _EVENT_TYPE_LABELS.get(r.event_type, r.event_type),
                    "count": r.count,
                }
                for r in rows
            ],
            "scene_stats": [],
        }

    @staticmethod
    async def get_ship_collision_fusion(
        db: AsyncSession,
        object_id: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        fusion_type: str = "ship_collision",
    ) -> list[dict]:
        """Get fusion analysis results for a specified fusion type."""
        # Verify object exists
        obj_result = await db.execute(
            select(ObjectInfo).where(ObjectInfo.object_id == object_id)
        )
        if not obj_result.scalar_one_or_none():
            raise NotFoundException(f"监测对象 {object_id} 不存在")

        query = select(FusionResult).where(
            FusionResult.object_id == object_id,
            FusionResult.fusion_type == fusion_type,
        )
        if start_time:
            query = query.where(FusionResult.fusion_time >= datetime.fromisoformat(start_time))
        if end_time:
            query = query.where(FusionResult.fusion_time <= datetime.fromisoformat(end_time))
        query = query.order_by(FusionResult.fusion_time.desc())

        result = await db.execute(query)
        fusion_results = result.scalars().all()

        return [
            {
                "fusion_id": f.fusion_id,
                "score": float(f.score) if f.score else None,
                "risk_level": f.risk_level,
                "rule_desc": f.rule_desc,
                "fusion_time": f.fusion_time.isoformat() if f.fusion_time else None,
                "related_event_id": f.related_event_id,
            }
            for f in fusion_results
        ]
