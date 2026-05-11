"""
API endpoints for Alert notifications (告警通知).
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.alerts import BatchAcknowledgeRequest
from app.services.alert_service import AlertService
from app.utils.pagination import PaginationParams
from app.utils.response import success_response

router = APIRouter()


@router.get("")
async def list_alerts(
    page_no: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """获取告警列表"""
    pagination = PaginationParams(page_no=page_no, page_size=page_size)
    items, total = await AlertService.list_alerts(
        db, pagination=pagination, status=status, severity=severity,
    )
    return success_response({
        "total": total,
        "page_no": page_no,
        "page_size": page_size,
        "list": items,
    })


@router.get("/unread-count")
async def unread_alert_count(
    db: AsyncSession = Depends(get_db),
):
    """获取未读告警数量"""
    data = await AlertService.get_unread_count(db)
    return success_response(data)


@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    db: AsyncSession = Depends(get_db),
):
    """确认单条告警"""
    data = await AlertService.acknowledge_alert(db, alert_id)
    return success_response(data)


@router.post("/batch-acknowledge")
async def batch_acknowledge_alerts(
    body: BatchAcknowledgeRequest,
    db: AsyncSession = Depends(get_db),
):
    """批量确认告警"""
    data = await AlertService.batch_acknowledge(db, body.alert_ids)
    return success_response(data)
