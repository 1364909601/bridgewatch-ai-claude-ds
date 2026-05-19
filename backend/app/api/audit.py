"""
API endpoints for Audit Logs (审计日志).
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user, require_role
from app.services.audit_service import AuditService
from app.utils.pagination import PaginationParams
from app.utils.response import success_response

router = APIRouter()


@router.get("")
async def list_audit_logs(
    page_no: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    log_type: Optional[str] = Query(None),
    log_level: Optional[str] = Query(None),
    user_id: Optional[str] = Query(None),
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("admin")),
):
    """获取审计日志列表（仅 admin）"""
    pagination = PaginationParams(page_no=page_no, page_size=page_size)
    items, total = await AuditService.list_logs(
        db, pagination=pagination,
        log_type=log_type, log_level=log_level,
        user_id=user_id, start_time=start_time, end_time=end_time,
    )
    return success_response({
        "total": total,
        "page_no": page_no,
        "page_size": page_size,
        "list": items,
    })
