from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.models.object_info import ObjectInfo
from app.utils.response import success_response

router = APIRouter()


@router.get("")
async def list_objects(
    object_type: Optional[str] = Query(None, description="对象类型: bridge/tunnel"),
    status: Optional[str] = Query(None, description="状态: active/inactive"),
    db: AsyncSession = Depends(get_db),
):
    query = select(ObjectInfo)
    if object_type:
        query = query.where(ObjectInfo.object_type == object_type)
    if status:
        query = query.where(ObjectInfo.status == status)
    query = query.order_by(ObjectInfo.object_name)

    result = await db.execute(query)
    objects = result.scalars().all()

    return success_response([{
        "object_id": o.object_id,
        "object_name": o.object_name,
        "object_type": o.object_type,
        "location_desc": o.location_desc,
        "status": o.status,
    } for o in objects])
