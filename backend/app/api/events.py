from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.event_record import EventRecord
from app.models.video_info import VideoInfo
from app.models.object_info import ObjectInfo
from app.utils.response import success_response, error_response
from app.utils.pagination import PaginationParams, paginated_response
from app.utils.exceptions import NotFoundException, BadRequestException

router = APIRouter()


@router.get("")
async def list_events(
    page_no: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    object_type: Optional[str] = Query(None),
    object_id: Optional[str] = Query(None),
    event_type: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    scene_type: Optional[str] = Query(None),
    review_status: Optional[str] = Query(None),
    video_name: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    pagination = PaginationParams(page_no, page_size)

    # Build base query — only join related tables when needed
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

    # Apply filters
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

    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Get paginated results
    base_query = base_query.order_by(EventRecord.event_time.desc())
    base_query = base_query.offset(pagination.offset).limit(pagination.limit)
    result = await db.execute(base_query)
    events = result.scalars().all()

    return success_response(paginated_response(
        [{
            "event_id": e.event_id,
            "object_id": e.object_id,
            "video_id": e.video_id,
            "event_type": e.event_type,
            "risk_level": e.risk_level,
            "scene_type": e.scene_type,
            "event_time": e.event_time.isoformat() if e.event_time else None,
            "start_second": e.start_second,
            "end_second": e.end_second,
            "thumbnail_url": e.thumbnail_url,
            "result_desc": e.result_desc,
            "review_status": e.review_status,
            "review_remark": e.review_remark,
        } for e in events],
        total,
        pagination,
    ))


@router.get("/{event_id}")
async def get_event_detail(
    event_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(EventRecord).where(EventRecord.event_id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise NotFoundException(f"事件 {event_id} 不存在")

    return success_response({
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
        "clip_url": event.clip_url,
        "result_desc": event.result_desc,
        "review_status": event.review_status,
        "review_remark": event.review_remark,
        "created_time": event.created_time.isoformat() if event.created_time else None,
        "updated_time": event.updated_time.isoformat() if event.updated_time else None,
    })


@router.post("/{event_id}/review")
async def review_event(
    event_id: str,
    body: dict,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(EventRecord).where(EventRecord.event_id == event_id))
    event = result.scalar_one_or_none()
    if not event:
        raise NotFoundException(f"事件 {event_id} 不存在")

    review_status = body.get("review_status")
    if review_status not in ("pending", "reviewed"):
        raise BadRequestException("复核状态必须为 pending 或 reviewed")

    event.review_status = review_status
    if "review_remark" in body:
        event.review_remark = body.get("review_remark")

    await db.commit()
    await db.refresh(event)

    return success_response({
        "event_id": event.event_id,
        "review_status": event.review_status,
        "review_remark": event.review_remark,
    })
