"""
API endpoints for Monitoring Data (监测数据).
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.monitoring_service import MonitoringService
from app.utils.response import success_response

router = APIRouter()


@router.get("")
async def list_monitoring_data(
    object_id: str = Query(..., description="监测对象ID"),
    data_types: Optional[str] = Query(None, description="数据类型，逗号分隔，如 co,lux,traffic"),
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """获取监测数据"""
    types_list = data_types.split(",") if data_types else None
    data = await MonitoringService.get_monitoring_data(
        db,
        object_id=object_id,
        data_types=types_list,
        start_time=start_time,
        end_time=end_time,
        limit=limit,
    )
    return success_response(data)
