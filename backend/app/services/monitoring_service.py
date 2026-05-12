"""
Service layer for Monitoring Data (监测数据).
"""

import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.monitoring_data import MonitoringData

logger = logging.getLogger(__name__)


class MonitoringService:
    """Business logic for querying sensor/monitoring data."""

    @staticmethod
    async def get_monitoring_data(
        db: AsyncSession,
        object_id: str,
        data_types: Optional[list[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 100,
    ) -> list[dict]:
        """Query monitoring data points with optional filters."""
        query = select(MonitoringData).where(
            MonitoringData.object_id == object_id
        )

        if data_types:
            query = query.where(MonitoringData.data_type.in_(data_types))
        if start_time:
            query = query.where(
                MonitoringData.data_time >= datetime.fromisoformat(start_time)
            )
        if end_time:
            query = query.where(
                MonitoringData.data_time <= datetime.fromisoformat(end_time)
            )

        query = query.order_by(MonitoringData.data_time.asc())
        query = query.limit(limit)

        result = await db.execute(query)
        points = result.scalars().all()

        return [
            {
                "data_id": p.data_id,
                "object_id": p.object_id,
                "data_type": p.data_type,
                "data_value": float(p.data_value) if p.data_value is not None else 0,
                "data_time": p.data_time.isoformat() if p.data_time else None,
                "ext_json": p.ext_json,
            }
            for p in points
        ]
