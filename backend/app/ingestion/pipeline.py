"""
Data ingestion pipeline — collect, transform, and store external data.

Pipeline flow:
  External source → Connector.collect() → transform → MonitoringData / EventRecord / VideoInfo
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory
from app.ingestion.connectors import (
    AisReceiver,
    ShmSensorConnector,
    TunnelEnvironmentSensor,
    VideoStreamIngester,
)
from app.models.monitoring_data import MonitoringData
from app.models.video_info import VideoInfo
from app.utils.id_generator import IDGenerator

logger = logging.getLogger(__name__)


class IngestionPipeline:
    """
    Orchestrates data collection from all sources and persists to database.

    Usage:
        pipeline = IngestionPipeline()
        await pipeline.run_once(bridge_id="OBJ-BR-001", tunnel_id="OBJ-TN-001")
    """

    def __init__(self):
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def run_once(
        self,
        bridge_id: str = "OBJ-20260508-001",
        large_bridge_id: str = "OBJ-20260508-003",
        tunnel_id: str = "OBJ-20260508-004",
    ) -> dict[str, int]:
        """
        Collect data from all simulated sources and store in database.
        Returns count of records created per source type.
        """
        counts: dict[str, int] = {"shm": 0, "ais": 0, "tunnel": 0, "video": 0}

        async with async_session_factory() as db:
            # 1. SHM sensors
            shm = ShmSensorConnector(bridge_id)
            for point in await shm.collect():
                db.add(MonitoringData(**point))
                counts["shm"] += 1

            # 2. AIS receiver (large bridges)
            ais = AisReceiver(large_bridge_id)
            for point in await ais.collect():
                ext = point.pop("ext_json", None)
                db.add(MonitoringData(**point, ext_json=ext))
                counts["ais"] += 1

            # 3. Tunnel environment
            tunnel = TunnelEnvironmentSensor(tunnel_id)
            for point in await tunnel.collect():
                db.add(MonitoringData(**point))
                counts["tunnel"] += 1

            # 4. Video stream
            video = VideoStreamIngester(bridge_id)
            info = await video.collect()
            existing = await db.get(VideoInfo, info["video_name"])
            if not existing:
                db.add(VideoInfo(
                    video_id=IDGenerator.generate_unique("VID"),
                    **info,
                ))
                counts["video"] += 1

            await db.commit()

        logger.info("Ingestion complete: %s", counts)
        return counts

    async def start(self, interval: int = 300) -> None:
        """Start periodic ingestion every ``interval`` seconds."""
        self._running = True
        self._task = asyncio.create_task(self._loop(interval))
        logger.info("Ingestion pipeline started (interval=%ds)", interval)

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _loop(self, interval: int) -> None:
        while self._running:
            try:
                await self.run_once()
            except Exception:
                logger.exception("Ingestion cycle failed")
            await asyncio.sleep(interval)
