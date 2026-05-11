"""
Service layer for Events (事件中心).
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event_record import EventRecord
from app.models.video_info import VideoInfo
from app.models.object_info import ObjectInfo
from app.utils.exceptions import NotFoundException, BadRequestException
from app.utils.pagination import PaginationParams


_EVENT_TYPE_LABELS = {
    "collapse": "桥梁坍塌",
    "deformation": "桥面大变形",
    "congestion": "车辆积压",
    "fire": "桥面火灾",
    "ship_collision": "船舶碰撞",
}


class EventService:
    """Business logic for event operations."""

    @staticmethod
    def _to_dict(event: EventRecord) -> dict:
        return {
            "event_id": event.event_id,
            "object_id": event.object_id,
            "video_id": event.video_id,
            "event_type": event.event_type,
            "risk_level": event.risk_level,
            "scene_type": event.scene_type,
            "event_time": event.event_time.isoformat() if event.event_time else None,
            "start_second": event.start_second,
            "end_second": event.end_second,
            "thumbnail_url": event.thumbnail_url,
            "result_desc": event.result_desc,
            "review_status": event.review_status,
            "review_remark": event.review_remark,
        }

    @staticmethod
    def _to_detail_dict(event: EventRecord) -> dict:
        d = EventService._to_dict(event)
        d.update({
            "clip_url": event.clip_url,
            "created_time": event.created_time.isoformat() if event.created_time else None,
            "updated_time": event.updated_time.isoformat() if event.updated_time else None,
        })
        return d

    @staticmethod
    async def list_events(
        db: AsyncSession,
        pagination: PaginationParams,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        object_type: Optional[str] = None,
        object_id: Optional[str] = None,
        event_type: Optional[str] = None,
        risk_level: Optional[str] = None,
        scene_type: Optional[str] = None,
        review_status: Optional[str] = None,
        video_name: Optional[str] = None,
    ) -> tuple[list[dict], int]:
        """List events with multi-condition filtering."""
        base_query = select(EventRecord)
        count_query = select(func.count()).select_from(EventRecord)

        need_video_join = bool(video_name)
        need_object_join = bool(object_type)

        if need_video_join:
            base_query = base_query.join(VideoInfo, EventRecord.video_id == VideoInfo.video_id)
            count_query = count_query.join(VideoInfo, EventRecord.video_id == VideoInfo.video_id)
        if need_object_join:
            base_query = base_query.join(ObjectInfo, EventRecord.object_id == ObjectInfo.object_id)
            count_query = count_query.join(ObjectInfo, EventRecord.object_id == ObjectInfo.object_id)

        if start_time:
            dt = datetime.fromisoformat(start_time)
            base_query = base_query.where(EventRecord.event_time >= dt)
            count_query = count_query.where(EventRecord.event_time >= dt)
        if end_time:
            dt = datetime.fromisoformat(end_time)
            base_query = base_query.where(EventRecord.event_time <= dt)
            count_query = count_query.where(EventRecord.event_time <= dt)
        if object_id:
            base_query = base_query.where(EventRecord.object_id == object_id)
            count_query = count_query.where(EventRecord.object_id == object_id)
        if object_type:
            base_query = base_query.where(ObjectInfo.object_type == object_type)
            count_query = count_query.where(ObjectInfo.object_type == object_type)
        if risk_level:
            base_query = base_query.where(EventRecord.risk_level == risk_level)
            count_query = count_query.where(EventRecord.risk_level == risk_level)
        if scene_type:
            base_query = base_query.where(EventRecord.scene_type == scene_type)
            count_query = count_query.where(EventRecord.scene_type == scene_type)
        if review_status:
            base_query = base_query.where(EventRecord.review_status == review_status)
            count_query = count_query.where(EventRecord.review_status == review_status)
        if event_type:
            types = [t.strip() for t in event_type.split(",")]
            base_query = base_query.where(EventRecord.event_type.in_(types))
            count_query = count_query.where(EventRecord.event_type.in_(types))
        if video_name:
            base_query = base_query.where(VideoInfo.video_name.ilike(f"%{video_name}%"))
            count_query = count_query.where(VideoInfo.video_name.ilike(f"%{video_name}%"))

        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        base_query = base_query.order_by(EventRecord.event_time.desc())
        base_query = base_query.offset(pagination.offset).limit(pagination.limit)
        result = await db.execute(base_query)
        events = result.scalars().all()

        event_dicts = [EventService._to_dict(e) for e in events]
        # Batch-enrich with object_name and video_name
        obj_ids = list({e["object_id"] for e in event_dicts if e.get("object_id")})
        vid_ids = list({e["video_id"] for e in event_dicts if e.get("video_id")})
        obj_map: dict[str, str] = {}
        if obj_ids:
            r = await db.execute(
                select(ObjectInfo.object_id, ObjectInfo.object_name).where(
                    ObjectInfo.object_id.in_(obj_ids)
                )
            )
            for row in r.all():
                obj_map[row.object_id] = row.object_name
        vid_map: dict[str, str] = {}
        if vid_ids:
            r = await db.execute(
                select(VideoInfo.video_id, VideoInfo.video_name).where(
                    VideoInfo.video_id.in_(vid_ids)
                )
            )
            for row in r.all():
                vid_map[row.video_id] = row.video_name
        for e in event_dicts:
            e["object_name"] = obj_map.get(e.get("object_id", ""), e.get("object_id"))
            e["video_name"] = vid_map.get(e.get("video_id", ""), e.get("video_id"))
        return event_dicts, total

    @staticmethod
    async def get_event_detail(db: AsyncSession, event_id: str) -> dict:
        """Get full event detail."""
        result = await db.execute(
            select(EventRecord).where(EventRecord.event_id == event_id)
        )
        event = result.scalar_one_or_none()
        if not event:
            raise NotFoundException(f"事件 {event_id} 不存在")
        d = EventService._to_detail_dict(event)
        # Enrich with object_name and video_name
        obj_r = await db.execute(
            select(ObjectInfo.object_name).where(ObjectInfo.object_id == event.object_id)
        )
        obj = obj_r.scalar_one_or_none()
        d["object_name"] = obj or event.object_id
        vid_r = await db.execute(
            select(VideoInfo.video_name).where(VideoInfo.video_id == event.video_id)
        )
        vid = vid_r.scalar_one_or_none()
        d["video_name"] = vid or event.video_id
        return d

    @staticmethod
    async def review_event(
        db: AsyncSession,
        event_id: str,
        review_status: str,
        review_remark: Optional[str] = None,
    ) -> dict:
        """Review (approve/reject) an event."""
        result = await db.execute(
            select(EventRecord).where(EventRecord.event_id == event_id)
        )
        event = result.scalar_one_or_none()
        if not event:
            raise NotFoundException(f"事件 {event_id} 不存在")

        if review_status not in ("pending", "reviewed"):
            raise BadRequestException("复核状态必须为 pending 或 reviewed")

        event.review_status = review_status
        if review_remark is not None:
            event.review_remark = review_remark

        await db.commit()
        await db.refresh(event)

        return {
            "event_id": event.event_id,
            "review_status": event.review_status,
            "review_remark": event.review_remark,
        }
