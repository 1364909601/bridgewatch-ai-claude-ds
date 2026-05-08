"""
Service layer for Videos (视频管理).
"""

from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.video_info import VideoInfo
from app.models.event_record import EventRecord
from app.utils.exceptions import NotFoundException
from app.utils.pagination import PaginationParams


class VideoService:
    """Business logic for video operations."""

    @staticmethod
    async def list_videos(
        db: AsyncSession,
        pagination: PaginationParams,
        object_id: Optional[str] = None,
        scene_type: Optional[str] = None,
    ) -> tuple[list[dict], int]:
        """List videos with optional filters."""
        query = select(VideoInfo)
        count_query = select(func.count()).select_from(VideoInfo)

        if object_id:
            query = query.where(VideoInfo.object_id == object_id)
            count_query = count_query.where(VideoInfo.object_id == object_id)
        if scene_type:
            query = query.where(VideoInfo.scene_type == scene_type)
            count_query = count_query.where(VideoInfo.scene_type == scene_type)

        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(VideoInfo.capture_time.desc())
        query = query.offset(pagination.offset).limit(pagination.limit)
        result = await db.execute(query)
        videos = result.scalars().all()

        return [
            {
                "video_id": v.video_id,
                "object_id": v.object_id,
                "video_name": v.video_name,
                "file_url": v.file_url,
                "capture_time": v.capture_time.isoformat() if v.capture_time else None,
                "duration_seconds": v.duration_seconds,
                "resolution": v.resolution,
                "scene_type": v.scene_type,
                "preprocess_status": v.preprocess_status,
            }
            for v in videos
        ], total

    @staticmethod
    async def get_video_events(
        db: AsyncSession,
        video_id: str,
    ) -> list[dict]:
        """Get all events associated with a video."""
        video_result = await db.execute(
            select(VideoInfo).where(VideoInfo.video_id == video_id)
        )
        if not video_result.scalar_one_or_none():
            raise NotFoundException(f"视频 {video_id} 不存在")

        result = await db.execute(
            select(EventRecord)
            .where(EventRecord.video_id == video_id)
            .order_by(EventRecord.start_second)
        )
        events = result.scalars().all()

        return [
            {
                "event_id": e.event_id,
                "event_type": e.event_type,
                "risk_level": e.risk_level,
                "start_second": e.start_second,
                "end_second": e.end_second,
            }
            for e in events
        ]

    @staticmethod
    async def get_video_play_url(
        db: AsyncSession,
        video_id: str,
    ) -> dict:
        """Get video play URL."""
        result = await db.execute(
            select(VideoInfo).where(VideoInfo.video_id == video_id)
        )
        video = result.scalar_one_or_none()
        if not video:
            raise NotFoundException(f"视频 {video_id} 不存在")

        return {
            "video_id": video.video_id,
            "play_url": video.file_url,
            "duration_seconds": video.duration_seconds,
        }
