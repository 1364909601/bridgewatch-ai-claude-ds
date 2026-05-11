"""
Background worker: polls the inference_task table for queued tasks
and processes them using the detection pipeline.
"""

import asyncio
import logging
import traceback
from datetime import datetime

from sqlalchemy import select

from app.database import async_session_factory
from app.models.event_record import EventRecord
from app.models.inference_task import InferenceTask
from app.models.object_info import ObjectInfo
from app.models.video_info import VideoInfo
from app.engine.detector import run_detection_pipeline
from app.services.alert_service import AlertService
from app.utils.id_generator import generate_event_id

logger = logging.getLogger(__name__)


class InferenceWorker:
    """
    Simple polling worker that runs as an asyncio background task.

    Fetches the oldest queued inference task, runs the detection pipeline
    on the associated video, and creates EventRecord rows for each detection.
    """

    def __init__(self, poll_interval: int = 5) -> None:
        self._poll_interval = poll_interval
        self._running = False
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        """Register the worker loop as a background asyncio Task."""
        self._running = True
        self._task = asyncio.create_task(self._loop(), name="inference-worker")
        logger.info("InferenceWorker started (poll_interval=%ds)", self._poll_interval)

    async def stop(self) -> None:
        """Signal the worker to stop and await its completion."""
        self._running = False
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("InferenceWorker stopped")

    async def _loop(self) -> None:
        """Main polling loop."""
        while self._running:
            try:
                await self._poll_once()
            except asyncio.CancelledError:
                logger.info("InferenceWorker cancelled, exiting loop")
                break
            except Exception:
                logger.exception("InferenceWorker poll iteration failed")
            await asyncio.sleep(self._poll_interval)

    async def _poll_once(self) -> None:
        """Single poll: fetch one queued task and process it."""
        async with async_session_factory() as db:
            result = await db.execute(
                select(InferenceTask)
                .where(InferenceTask.task_status == "queued")
                .order_by(InferenceTask.created_time.asc())
                .limit(1)
            )
            task = result.scalar_one_or_none()
            if task is None:
                return

            # Transition to running
            task.task_status = "running"
            task.start_time = datetime.utcnow()
            await db.commit()
            logger.info("Task %s started (video=%s)", task.task_id, task.video_id)

        # Process in a separate session (longer-lived work)
        try:
            await self._process_task(task)
        except Exception:
            logger.exception("Task %s failed", task.task_id)
            async with async_session_factory() as db:
                db_task = await db.get(InferenceTask, task.task_id)
                if db_task:
                    db_task.task_status = "failed"
                    db_task.end_time = datetime.utcnow()
                    db_task.error_message = traceback.format_exc()
                    await db.commit()

    async def _process_task(self, task: InferenceTask) -> None:
        """
        Core processing: load video, run detection pipeline, persist events.
        """
        async with async_session_factory() as db:
            video = await db.get(VideoInfo, task.video_id)
            if video is None:
                raise ValueError(f"Video {task.video_id} not found for task {task.task_id}")

            obj = await db.get(ObjectInfo, video.object_id)
            if obj is None:
                raise ValueError(f"Object {video.object_id} not found for task {task.task_id}")

            # Run detection pipeline
            results = run_detection_pipeline(video, obj)

            # Create EventRecord for each detection result
            created_events: list[EventRecord] = []
            for det in results:
                event = EventRecord(
                    event_id=generate_event_id(),
                    object_id=video.object_id,
                    video_id=video.video_id,
                    event_type=det.event_type,
                    risk_level=det.risk_level,
                    scene_type=det.scene_type,
                    event_time=datetime.utcnow(),
                    start_second=det.start_second,
                    end_second=det.end_second,
                    result_desc=det.result_desc,
                    review_status="pending",
                )
                db.add(event)
                created_events.append(event)

            # Flush to get event IDs, then evaluate alerts
            if created_events:
                await db.flush()
                for event in created_events:
                    await AlertService.evaluate_new_event(db, event)

            # Update task status
            db_task = await db.get(InferenceTask, task.task_id)
            if db_task:
                db_task.task_status = "success"
                db_task.end_time = datetime.utcnow()
                if created_events:
                    db_task.result_summary = (
                        f"检测到 {len(created_events)} 个事件: "
                        + ", ".join(f"{r.event_type}={r.risk_level}" for r in results)
                    )
                else:
                    db_task.result_summary = "未检测到异常事件"

            await db.commit()

            if created_events:
                logger.info(
                    "Task %s completed: %d event(s): %s",
                    task.task_id,
                    len(created_events),
                    [(r.event_type, r.risk_level) for r in results],
                )
            else:
                logger.info("Task %s completed: no events detected", task.task_id)
