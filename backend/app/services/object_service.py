"""
Service layer for Objects (监测对象).
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.object_info import ObjectInfo


class ObjectService:
    """Business logic for monitoring object CRUD."""

    @staticmethod
    async def list_objects(
        db: AsyncSession,
        object_type: Optional[str] = None,
        status: Optional[str] = None,
    ) -> list[dict]:
        """List objects with optional filters."""
        query = select(ObjectInfo)
        if object_type:
            query = query.where(ObjectInfo.object_type == object_type)
        if status:
            query = query.where(ObjectInfo.status == status)
        query = query.order_by(ObjectInfo.object_name)

        result = await db.execute(query)
        objects = result.scalars().all()

        return [
            {
                "object_id": o.object_id,
                "object_name": o.object_name,
                "object_type": o.object_type,
                "location_desc": o.location_desc,
                "status": o.status,
            }
            for o in objects
        ]

    @staticmethod
    async def get_by_id(db: AsyncSession, object_id: str) -> Optional[ObjectInfo]:
        """Get a single object by ID."""
        result = await db.execute(
            select(ObjectInfo).where(ObjectInfo.object_id == object_id)
        )
        return result.scalar_one_or_none()
