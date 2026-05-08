from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database import get_db
from app.schemas.objects import ObjectResponse
from app.services.object_service import ObjectService
from app.utils.response import success_response

router = APIRouter()

# Type alias for list response
ObjectListResponse = list[ObjectResponse]


@router.get("")
async def list_objects(
    object_type: Optional[str] = Query(None, description="对象类型: bridge/tunnel"),
    status: Optional[str] = Query(None, description="状态: active/inactive"),
    db: AsyncSession = Depends(get_db),
):
    """获取监测对象列表"""
    objects = await ObjectService.list_objects(
        db, object_type=object_type, status=status
    )
    return success_response(objects)
