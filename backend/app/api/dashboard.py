from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.event_record import EventRecord
from app.models.object_info import ObjectInfo
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
    query = select(
        func.count().label("total"),
        func.sum(case((EventRecord.risk_level == "high", 1), else_=0)).label("high_risk"),
        func.sum(case((ObjectInfo.object_type == "bridge", 1), else_=0)).label("bridges"),
        func.sum(case((ObjectInfo.object_type == "tunnel", 1), else_=0)).label("tunnels"),
    ).join(ObjectInfo, EventRecord.object_id == ObjectInfo.object_id)

    if start_time:
        query = query.where(EventRecord.event_time >= datetime.fromisoformat(start_time))
    if end_time:
        query = query.where(EventRecord.event_time <= datetime.fromisoformat(end_time))
    if object_id:
        query = query.where(EventRecord.object_id == object_id)
    if object_type:
        query = query.where(ObjectInfo.object_type == object_type)
    if scene_type:
        query = query.where(EventRecord.scene_type == scene_type)

    result = await db.execute(query)
    row = result.one()

    return success_response({
        "total": row.total or 0,
        "high_risk": row.high_risk or 0,
        "bridges": row.bridges or 0,
        "tunnels": row.tunnels or 0,
    })


@router.get("/trend")
async def dashboard_trend(
    days: int = Query(7, ge=1, le=90),
    object_type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    since = datetime.utcnow() - timedelta(days=days)

    day_col = func.date(EventRecord.event_time)

    query = select(
        day_col.label("date"),
        func.count().label("count"),
        func.sum(case((EventRecord.risk_level == "high", 1), else_=0)).label("high_risk"),
    ).where(
        EventRecord.event_time >= since
    ).group_by(
        day_col
    ).order_by(day_col)

    result = await db.execute(query)
    rows = result.all()

    return success_response([{
        "date": str(r.date),
        "count": r.count,
        "high_risk": r.high_risk or 0,
    } for r in rows])


@router.get("/distribution")
async def dashboard_distribution(
    db: AsyncSession = Depends(get_db),
):
    query = select(
        EventRecord.event_type,
        func.count().label("count"),
    ).group_by(
        EventRecord.event_type
    ).order_by(
        EventRecord.event_type
    )

    result = await db.execute(query)
    rows = result.all()

    type_labels = {
        "collapse": "桥梁坍塌",
        "deformation": "桥面大变形",
        "congestion": "车辆积压",
        "fire": "桥面火灾",
        "ship_collision": "船舶碰撞",
    }

    return success_response([{
        "event_type": r.event_type,
        "event_type_name": type_labels.get(r.event_type, r.event_type),
        "count": r.count,
    } for r in rows])
