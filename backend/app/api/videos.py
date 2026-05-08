from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.video_info import VideoInfo
from app.models.event_record import EventRecord
from app.utils.response import success_response
from app.utils.pagination import PaginationParams, paginated_response
from app.utils.exceptions import NotFoundException

router = APIRouter()


@router.get("")
async def list_videos(
    page_no: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    object_id: Optional[str] = Query(None),
    scene_type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    pagination = PaginationParams(page_no, page_size)

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

    return success_response(paginated_response(
        [{
            "video_id": v.video_id,
            "object_id": v.object_id,
            "video_name": v.video_name,
            "file_url": v.file_url,
            "capture_time": v.capture_time.isoformat() if v.capture_time else None,
            "duration_seconds": v.duration_seconds,
            "resolution": v.resolution,
            "scene_type": v.scene_type,
            "preprocess_status": v.preprocess_status,
        } for v in videos],
        total,
        pagination,
    ))


@router.get("/{video_id}/events")
async def get_video_events(
    video_id: str,
    db: AsyncSession = Depends(get_db),
):
    # Verify video exists
    video_result = await db.execute(select(VideoInfo).where(VideoInfo.video_id == video_id))
    if not video_result.scalar_one_or_none():
        raise NotFoundException(f"视频 {video_id} 不存在")

    result = await db.execute(
        select(EventRecord)
        .where(EventRecord.video_id == video_id)
        .order_by(EventRecord.start_second)
    )
    events = result.scalars().all()

    return success_response([{
        "event_id": e.event_id,
        "event_type": e.event_type,
        "risk_level": e.risk_level,
        "start_second": e.start_second,
        "end_second": e.end_second,
    } for e in events])


@router.get("/{video_id}/play-url")
async def get_video_play_url(
    video_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(VideoInfo).where(VideoInfo.video_id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        raise NotFoundException(f"视频 {video_id} 不存在")

    # Phase 2: return stored file_url as play URL
    # Phase 3+: generate signed URL or HLS streaming URL
    return success_response({
        "video_id": video.video_id,
        "play_url": video.file_url,
        "duration_seconds": video.duration_seconds,
    })
