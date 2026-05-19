"""
Service layer for Dashboard (总览面板).
"""

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event_record import EventRecord
from app.models.object_info import ObjectInfo


_EVENT_TYPE_LABELS = {
    "collapse": "桥梁坍塌",
    "deformation": "桥面大变形",
    "congestion": "车辆积压",
    "fire": "桥面火灾",
    "ship_collision": "船舶碰撞",
}


class DashboardService:
    """Business logic for dashboard statistics."""

    @staticmethod
    async def get_summary(
        db: AsyncSession,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        object_type: Optional[str] = None,
        object_id: Optional[str] = None,
        scene_type: Optional[str] = None,
    ) -> dict:
        """Get dashboard summary (total events, high risk, bridge/tunnel counts)."""
        # Count total objects by type (from ObjectInfo directly, not joined with events)
        obj_type_result = await db.execute(
            select(
                func.sum(case((ObjectInfo.object_type == "bridge", 1), else_=0)).label("bridges"),
                func.sum(case((ObjectInfo.object_type == "tunnel", 1), else_=0)).label("tunnels"),
            )
        )
        obj_row = obj_type_result.one()
        total_objects = (obj_row.bridges or 0) + (obj_row.tunnels or 0)

        query = select(
            func.count().label("total"),
            func.sum(case((EventRecord.risk_level == "high", 1), else_=0)).label("high_risk"),
            func.sum(case((EventRecord.risk_level == "medium", 1), else_=0)).label("medium_risk"),
            func.sum(case((EventRecord.risk_level == "low", 1), else_=0)).label("low_risk"),
        )

        if object_id or object_type:
            query = query.select_from(EventRecord).join(ObjectInfo, EventRecord.object_id == ObjectInfo.object_id)

        if start_time:
            query = query.where(EventRecord.event_time >= datetime.fromisoformat(start_time))
        if end_time:
            query = query.where(EventRecord.event_time <= datetime.fromisoformat(end_time))
        if object_id:
            query = query.where(EventRecord.object_id == object_id)
        if object_type:
            query = query.where(ObjectInfo.object_type == object_type)
        if scene_type:
            query = query.where(EventRecord.scene_type == scene_type)

        result = await db.execute(query)
        row = result.one()

        return {
            "total": row.total or 0,
            "high_risk": row.high_risk or 0,
            "medium_risk": row.medium_risk or 0,
            "low_risk": row.low_risk or 0,
            "bridges": obj_row.bridges or 0,
            "tunnels": obj_row.tunnels or 0,
            "total_objects": total_objects,
        }

    @staticmethod
    async def get_trend(
        db: AsyncSession,
        days: int = 7,
        object_type: Optional[str] = None,
    ) -> list[dict]:
        """Get event trend over the past N days."""
        since = datetime.utcnow() - timedelta(days=days)

        day_col = func.date(EventRecord.event_time)
        query = select(
            day_col.label("date"),
            func.count().label("count"),
            func.sum(case((EventRecord.risk_level == "high", 1), else_=0)).label("high_risk"),
        ).where(EventRecord.event_time >= since)

        if object_type:
            query = query.join(ObjectInfo, EventRecord.object_id == ObjectInfo.object_id)
            query = query.where(ObjectInfo.object_type == object_type)

        query = query.group_by(day_col).order_by(day_col)

        result = await db.execute(query)
        rows = result.all()

        return [
            {
                "date": str(r.date),
                "count": r.count,
                "high_risk": r.high_risk or 0,
            }
            for r in rows
        ]

    @staticmethod
    async def get_distribution(
        db: AsyncSession,
    ) -> list[dict]:
        """Get event type distribution."""
        query = select(
            EventRecord.event_type,
            func.count().label("count"),
        ).group_by(EventRecord.event_type).order_by(EventRecord.event_type)

        result = await db.execute(query)
        rows = result.all()

        return [
            {
                "event_type": r.event_type,
                "event_type_name": _EVENT_TYPE_LABELS.get(r.event_type, r.event_type),
                "count": r.count,
            }
            for r in rows
        ]
