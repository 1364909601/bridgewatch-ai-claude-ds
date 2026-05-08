from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    DashboardTrendPoint,
    DashboardDistributionItem,
)
from app.services.dashboard_service import DashboardService
from app.utils.response import success_response

router = APIRouter()


@router.get("/summary")
async def dashboard_summary(
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    object_type: Optional[str] = Query(None),
    object_id: Optional[str] = Query(None),
    scene_type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """获取总览面板汇总统计"""
    data = await DashboardService.get_summary(
        db,
        start_time=start_time,
        end_time=end_time,
        object_type=object_type,
        object_id=object_id,
        scene_type=scene_type,
    )
    return success_response(data)


@router.get("/trend")
async def dashboard_trend(
    days: int = Query(7, ge=1, le=90),
    object_type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """获取事件趋势数据"""
    data = await DashboardService.get_trend(
        db, days=days, object_type=object_type
    )
    return success_response(data)


@router.get("/distribution")
async def dashboard_distribution(
    db: AsyncSession = Depends(get_db),
):
    """获取事件类型分布"""
    data = await DashboardService.get_distribution(db)
    return success_response(data)
