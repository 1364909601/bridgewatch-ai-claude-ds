from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.inference_task import InferenceTask
from app.utils.response import success_response
from app.utils.pagination import PaginationParams, paginated_response
from app.utils.id_generator import generate_task_id

router = APIRouter()


@router.post("/inference")
async def create_inference_task(
    body: dict,
    db: AsyncSession = Depends(get_db),
):
    task = InferenceTask(
        task_id=generate_task_id(),
        video_id=body.get("video_id", ""),
        model_id=body.get("model_id", ""),
        task_name=body.get("task_name", f"推理任务-{datetime.now().strftime('%Y%m%d%H%M%S')}"),
        task_status="queued",
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)

    return success_response({
        "task_id": task.task_id,
        "task_name": task.task_name,
        "task_status": task.task_status,
        "created_time": task.created_time.isoformat() if task.created_time else None,
    })


@router.get("/inference")
async def list_inference_tasks(
    page_no: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    task_status: Optional[str] = Query(None),
    video_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    pagination = PaginationParams(page_no, page_size)

    query = select(InferenceTask)
    count_query = select(func.count()).select_from(InferenceTask)

    if task_status:
        query = query.where(InferenceTask.task_status == task_status)
        count_query = count_query.where(InferenceTask.task_status == task_status)
    if video_id:
        query = query.where(InferenceTask.video_id == video_id)
        count_query = count_query.where(InferenceTask.video_id == video_id)

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.order_by(InferenceTask.created_time.desc())
    query = query.offset(pagination.offset).limit(pagination.limit)
    result = await db.execute(query)
    tasks = result.scalars().all()

    return success_response(paginated_response(
        [{
            "task_id": t.task_id,
            "video_id": t.video_id,
            "model_id": t.model_id,
            "task_name": t.task_name,
            "task_status": t.task_status,
            "start_time": t.start_time.isoformat() if t.start_time else None,
            "end_time": t.end_time.isoformat() if t.end_time else None,
            "result_summary": t.result_summary,
            "error_message": t.error_message,
            "created_time": t.created_time.isoformat() if t.created_time else None,
        } for t in tasks],
        total,
        pagination,
    ))
