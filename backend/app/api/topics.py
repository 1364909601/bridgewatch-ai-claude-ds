from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.event_record import EventRecord
from app.models.fusion_result import FusionResult
from app.models.object_info import ObjectInfo
from app.utils.response import success_response
from app.utils.exceptions import NotFoundException

router = APIRouter()


@router.get("/bridge/summary")
async def bridge_topic_summary(
    object_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns summary statistics for ordinary bridges:
    - event counts by type
    - scene-based assessment data
    """
    query = select(
        EventRecord.event_type,
        func.count().label("count"),
    )

    if object_id:
        query = query.where(EventRecord.object_id == object_id)

    query = query.group_by(EventRecord.event_type).order_by(EventRecord.event_type)
    result = await db.execute(query)
    rows = result.all()

    type_labels = {
        "collapse": "桥梁坍塌",
        "deformation": "桥面大变形",
        "congestion": "车辆积压",
        "fire": "桥面火灾",
    }

    return success_response({
        "event_type_stats": [{
            "event_type": r.event_type,
            "event_type_name": type_labels.get(r.event_type, r.event_type),
            "count": r.count,
        } for r in rows],
        "scene_stats": [],  # Phase 2 placeholder — needs algorithm evaluation data
    })


@router.get("/ship-collision/fusion")
async def ship_collision_fusion(
    object_id: str = Query(..., description="长大桥梁对象ID"),
    start_time: Optional[str] = Query(None),
    end_time: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Returns ship collision fusion analysis for large bridges:
    - fusion results with scores
    - ship tracks and monitoring data
    """
    # Verify object exists and is a bridge
    obj_result = await db.execute(
        select(ObjectInfo).where(
            ObjectInfo.object_id == object_id,
            ObjectInfo.object_type == "bridge",
        )
    )
    if not obj_result.scalar_one_or_none():
        raise NotFoundException(f"桥梁对象 {object_id} 不存在")

    query = select(FusionResult).where(
        FusionResult.object_id == object_id,
        FusionResult.fusion_type == "ship_collision",
    )
    if start_time:
        query = query.where(FusionResult.fusion_time >= datetime.fromisoformat(start_time))
    if end_time:
        query = query.where(FusionResult.fusion_time <= datetime.fromisoformat(end_time))
    query = query.order_by(FusionResult.fusion_time.desc())

    result = await db.execute(query)
    fusion_results = result.scalars().all()

    return success_response([{
        "fusion_id": f.fusion_id,
        "score": float(f.score) if f.score else None,
        "risk_level": f.risk_level,
        "rule_desc": f.rule_desc,
        "fusion_time": f.fusion_time.isoformat() if f.fusion_time else None,
        "related_event_id": f.related_event_id,
    } for f in fusion_results])
