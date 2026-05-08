from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.topics import BridgeSummaryResponse, FusionResultResponse
from app.services.topic_service import TopicService
from app.utils.response import success_response

router = APIRouter()


@router.get("/bridge/summary")
async def bridge_topic_summary(
    object_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    普通桥梁专题汇总统计
    - 按事件类型的统计
    - 场景评估数据
    """
    data = await TopicService.get_bridge_summary(db, object_id=object_id)
    return success_response(data)


@router.get("/ship-collision/fusion")
async def ship_collision_fusion(
    object_id: str = Query(..., description="长大桥梁对象ID"),
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    船撞融合预警分析
    - 融合评分结果
    - 船迹与监测数据关联
    """
    data = await TopicService.get_ship_collision_fusion(
        db,
        object_id=object_id,
        start_time=start_time,
        end_time=end_time,
    )
    return success_response(data)
