from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.tasks import TaskCreateRequest, TaskResponse
from app.services.task_service import TaskService
from app.utils.response import success_response
from app.utils.pagination import PaginatedResponse, paginated_response

router = APIRouter()


@router.post("/inference")
async def create_inference_task(
    body: TaskCreateRequest,
    db: AsyncSession = Depends(get_db),
):
    """创建推理任务"""
    task = await TaskService.create_task(
        db,
        video_id=body.video_id,
        model_id=body.model_id,
        task_name=body.task_name,
    )
    return success_response(task)


@router.get("/inference")
async def list_inference_tasks(
    page_no: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    task_status: Optional[str] = Query(None),
    video_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """获取推理任务列表"""
    pagination = type("P", (), {"page_no": page_no, "page_size": page_size, "offset": (page_no - 1) * page_size, "limit": page_size})()

    items, total = await TaskService.list_tasks(
        db, pagination,
        task_status=task_status,
        video_id=video_id,
    )
    return success_response(paginated_response(items, total, pagination))
