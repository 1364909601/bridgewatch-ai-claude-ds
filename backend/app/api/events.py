from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.schemas.events import (
    EventQueryParams,
    EventResponse,
    EventDetailResponse,
    EventReviewRequest,
    EventReviewResponse,
)
from app.services.event_service import EventService
from app.utils.response import success_response
from app.utils.pagination import PaginatedResponse, paginated_response

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
    """获取事件列表（支持多条件组合查询）"""
    pagination = type("P", (), {"page_no": page_no, "page_size": page_size, "offset": (page_no - 1) * page_size, "limit": page_size})()

    items, total = await EventService.list_events(
        db, pagination,
        start_time=start_time,
        end_time=end_time,
        object_type=object_type,
        object_id=object_id,
        event_type=event_type,
        risk_level=risk_level,
        scene_type=scene_type,
        review_status=review_status,
        video_name=video_name,
    )
    return success_response(paginated_response(items, total, pagination))


@router.get("/{event_id}")
async def get_event_detail(
    event_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取事件详情"""
    event = await EventService.get_event_detail(db, event_id)
    return success_response(event)


@router.post("/{event_id}/review")
async def review_event(
    event_id: str,
    body: EventReviewRequest,
    db: AsyncSession = Depends(get_db),
):
    """复核事件"""
    result = await EventService.review_event(
        db, event_id,
        review_status=body.review_status,
        review_remark=body.review_remark,
    )
    return success_response(result)
