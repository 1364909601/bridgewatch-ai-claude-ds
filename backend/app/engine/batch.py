"""
Batch inference: create inference tasks for videos that have not been
recently processed, so the background worker picks them up.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select

from app.database import async_session_factory
from app.models.inference_task import InferenceTask
from app.models.model_version import ModelVersion
from app.models.object_info import ObjectInfo
from app.models.video_info import VideoInfo
from app.utils.id_generator import generate_task_id

logger = logging.getLogger(__name__)


async def create_batch_tasks(
    model_id: str,
    object_type: Optional[str] = None,
    max_videos: int = 50,
    recheck_hours: int = 24,
) -> int:
    """
    Find videos that are ready for inference but have no successful task
    within the last ``recheck_hours``, and create queued tasks for them.

    Returns the number of tasks created.
    """
    cutoff = datetime.utcnow() - timedelta(hours=recheck_hours)
    created = 0

    async with async_session_factory() as db:
        # Base query: only preprocessed videos
        query = select(VideoInfo).where(VideoInfo.preprocess_status == "done")

        # Optional filter by object type (bridge / tunnel)
        if object_type:
            query = (
                select(VideoInfo)
                .join(ObjectInfo, VideoInfo.object_id == ObjectInfo.object_id)
                .where(
                    VideoInfo.preprocess_status == "done",
                    ObjectInfo.object_type == object_type,
                )
            )

        # Exclude videos that already had a successful task within cutoff
        subq = (
            select(InferenceTask.video_id)
            .where(
                InferenceTask.task_status == "success",
                InferenceTask.end_time >= cutoff,
            )
        ).subquery()

        query = query.where(VideoInfo.video_id.notin_(select(subq)))
        query = query.limit(max_videos)

        result = await db.execute(query)
        videos = result.scalars().all()

        if not videos:
            logger.info("No eligible videos found for batch inference")
            return 0

        # Verify model exists
        model = await db.get(ModelVersion, model_id)
        if model is None:
            raise ValueError(f"Model {model_id} not found in database")

        # Create tasks
        now = datetime.utcnow()
        for video in videos:
            task = InferenceTask(
                task_id=generate_task_id(),
                video_id=video.video_id,
                model_id=model_id,
                task_name=f"批量推理-{video.video_name}-{now.strftime('%Y%m%d%H%M%S')}",
                task_status="queued",
            )
            db.add(task)
            created += 1

        await db.commit()

    logger.info("Created %d batch inference tasks (model=%s)", created, model_id)
    return created


def run_batch(
    model_id: str,
    object_type: Optional[str] = None,
    max_videos: int = 50,
    recheck_hours: int = 24,
) -> int:
    """Synchronous CLI entry point for ``python -m app.engine.batch``."""
    return asyncio.run(
        create_batch_tasks(
            model_id=model_id,
            object_type=object_type,
            max_videos=max_videos,
            recheck_hours=recheck_hours,
        )
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create batch inference tasks")
    parser.add_argument("--model-id", required=True, help="Model ID to use (e.g. MDL-BRIDGE-V1.0)")
    parser.add_argument("--object-type", default=None, help="bridge or tunnel (optional)")
    parser.add_argument("--max-videos", type=int, default=50, help="Max videos to process")
    parser.add_argument("--recheck-hours", type=int, default=24, help="Skip videos processed within this window")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    count = run_batch(
        model_id=args.model_id,
        object_type=args.object_type,
        max_videos=args.max_videos,
        recheck_hours=args.recheck_hours,
    )
    print(f"Created {count} batch inference tasks")
