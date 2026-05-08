from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.videos import (
    VideoQueryParams,
    VideoResponse,
    VideoEventMarkResponse,
    VideoPlayUrlResponse,
)
from app.services.video_service import VideoService
from app.utils.response import success_response
from app.utils.pagination import PaginatedResponse, paginated_response

router = APIRouter()


@router.get("")
async def list_videos(
    page_no: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    object_id: Optional[str] = Query(None),
    scene_type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """获取视频列表"""
    pagination = type("P", (), {"page_no": page_no, "page_size": page_size, "offset": (page_no - 1) * page_size, "limit": page_size})()

    items, total = await VideoService.list_videos(
        db, pagination,
        object_id=object_id,
        scene_type=scene_type,
    )
    return success_response(paginated_response(items, total, pagination))


@router.get("/{video_id}/events")
async def get_video_events(
    video_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取视频关联的事件标记"""
    events = await VideoService.get_video_events(db, video_id)
    return success_response(events)


@router.get("/{video_id}/play-url")
async def get_video_play_url(
    video_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取视频播放地址"""
    result = await VideoService.get_video_play_url(db, video_id)
    return success_response(result)
