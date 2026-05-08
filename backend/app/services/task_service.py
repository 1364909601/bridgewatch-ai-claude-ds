"""
Service layer for Inference Tasks (推理任务).
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inference_task import InferenceTask
from app.utils.pagination import PaginationParams
from app.utils.id_generator import generate_task_id


class TaskService:
    """Business logic for inference task operations."""

    @staticmethod
    async def create_task(
        db: AsyncSession,
        video_id: str,
        model_id: str,
        task_name: Optional[str] = None,
    ) -> dict:
        """Create a new inference task."""
        task = InferenceTask(
            task_id=generate_task_id(),
            video_id=video_id,
            model_id=model_id,
            task_name=task_name or f"推理任务-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            task_status="queued",
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)

        return {
            "task_id": task.task_id,
            "task_name": task.task_name,
            "task_status": task.task_status,
            "created_time": task.created_time.isoformat() if task.created_time else None,
        }

    @staticmethod
    async def list_tasks(
        db: AsyncSession,
        pagination: PaginationParams,
        task_status: Optional[str] = None,
        video_id: Optional[str] = None,
    ) -> tuple[list[dict], int]:
        """List inference tasks with optional filters."""
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

        return [
            {
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
            }
            for t in tasks
        ], total
