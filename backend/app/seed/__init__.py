"""
Seed data for BridgeWatch AI backend.
Run once after database creation to populate initial reference data.

Usage:
    python -m app.seed
"""

import asyncio
import logging
from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory
from app.models.object_info import ObjectInfo
from app.models.video_info import VideoInfo
from app.models.event_record import EventRecord
from app.models.model_version import ModelVersion
from app.models.fusion_result import FusionResult
from app.models.monitoring_data import MonitoringData

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
#  Seed data
# ──────────────────────────────────────────────

OBJECTS = [
    # 普通桥梁
    ObjectInfo(object_id="OBJ-BR-001", object_name="厦门演武大桥", object_type="bridge", location_desc="K12+300", status="active"),
    ObjectInfo(object_id="OBJ-BR-002", object_name="青岛胶州湾大桥", object_type="bridge", location_desc="K45+600", status="active"),
    ObjectInfo(object_id="OBJ-BR-003", object_name="杭州湾跨海大桥", object_type="bridge", location_desc="K78+200", status="active"),
    # 长大桥梁（船撞监测）
    ObjectInfo(object_id="OBJ-BR-LARGE-001", object_name="南京长江大桥", object_type="bridge", location_desc="K103+500", status="active"),
    ObjectInfo(object_id="OBJ-BR-LARGE-002", object_name="上海长江大桥", object_type="bridge", location_desc="K156+800", status="active"),
    # 隧道
    ObjectInfo(object_id="OBJ-TN-001", object_name="海沧隧道", object_type="tunnel", location_desc="K201+100", status="active"),
    ObjectInfo(object_id="OBJ-TN-002", object_name="翔安隧道", object_type="tunnel", location_desc="K245+400", status="active"),
]

VIDEOS = [
    VideoInfo(video_id="VID-20260424-001", object_id="OBJ-BR-001", video_name="厦门演武大桥_20260424_0700.mp4",
              file_url="/videos/stream/VID-20260424-001.m3u8", capture_time=datetime(2026, 4, 24, 7, 0, 0, tzinfo=timezone.utc),
              duration_seconds=1800, resolution="1920x1080", scene_type="day", preprocess_status="completed"),
    VideoInfo(video_id="VID-20260424-002", object_id="OBJ-BR-002", video_name="青岛胶州湾大桥_20260424_0800.mp4",
              file_url="/videos/stream/VID-20260424-002.m3u8", capture_time=datetime(2026, 4, 24, 8, 0, 0, tzinfo=timezone.utc),
              duration_seconds=3600, resolution="1920x1080", scene_type="day", preprocess_status="completed"),
    VideoInfo(video_id="VID-20260424-003", object_id="OBJ-BR-LARGE-001", video_name="南京长江大桥_20260424_0600.mp4",
              file_url="/videos/stream/VID-20260424-003.m3u8", capture_time=datetime(2026, 4, 24, 6, 0, 0, tzinfo=timezone.utc),
              duration_seconds=3600, resolution="3840x2160", scene_type="day", preprocess_status="completed"),
    VideoInfo(video_id="VID-20260424-004", object_id="OBJ-TN-001", video_name="海沧隧道_20260424_0900.mp4",
              file_url="/videos/stream/VID-20260424-004.m3u8", capture_time=datetime(2026, 4, 24, 9, 0, 0, tzinfo=timezone.utc),
              duration_seconds=1800, resolution="1920x1080", scene_type="day", preprocess_status="completed"),
    VideoInfo(video_id="VID-20260425-001", object_id="OBJ-BR-003", video_name="杭州湾跨海大桥_20260425_1900.mp4",
              file_url="/videos/stream/VID-20260425-001.m3u8", capture_time=datetime(2026, 4, 25, 19, 0, 0, tzinfo=timezone.utc),
              duration_seconds=1800, resolution="1920x1080", scene_type="night", preprocess_status="completed"),
]

EVENTS = [
    EventRecord(
        event_id="EVT-20260424-001", object_id="OBJ-BR-001", video_id="VID-20260424-001",
        event_type="fire", risk_level="high", scene_type="night",
        event_time=datetime(2026, 4, 24, 7, 15, 32, tzinfo=timezone.utc),
        start_second=932, end_second=958,
        thumbnail_url="/files/thumbnails/EVT-20260424-001.jpg",
        clip_url="/files/clips/EVT-20260424-001.mp4",
        result_desc="可见光与热源特征同时触发，检测到桥面明火区域，温升 +42℃，烟雾区域持续扩大。高风险事件，应立即复核。",
        review_status="pending",
    ),
    EventRecord(
        event_id="EVT-20260424-002", object_id="OBJ-BR-002", video_id="VID-20260424-002",
        event_type="congestion", risk_level="medium", scene_type="day",
        event_time=datetime(2026, 4, 24, 8, 22, 10, tzinfo=timezone.utc),
        start_second=1320, end_second=1380,
        thumbnail_url="/files/thumbnails/EVT-20260424-002.jpg",
        result_desc="车流密度 0.76，平均速度 18km/h，持续时间超过 60 秒，判定为车辆积压事件。",
        review_status="pending",
    ),
    EventRecord(
        event_id="EVT-20260424-003", object_id="OBJ-BR-LARGE-001", video_id="VID-20260424-003",
        event_type="ship_collision", risk_level="medium", scene_type="day",
        event_time=datetime(2026, 4, 24, 6, 45, 22, tzinfo=timezone.utc),
        start_second=2712, end_second=2750,
        thumbnail_url="/files/thumbnails/EVT-20260424-003.jpg",
        result_desc="AIS 偏航 +3.2°，通航净空 32.5m，船舶接近桥墩保护区，融合评分 72.5。",
        review_status="pending",
    ),
    EventRecord(
        event_id="EVT-20260424-004", object_id="OBJ-BR-001", video_id="VID-20260424-001",
        event_type="collapse", risk_level="high", scene_type="day",
        event_time=datetime(2026, 4, 24, 7, 28, 15, tzinfo=timezone.utc),
        start_second=1690, end_second=1720,
        result_desc="桥面局部几何形态发生突变，结构缺失面积超过阈值，连续 8 帧确认。高风险坍塌事件。",
        review_status="pending",
    ),
    EventRecord(
        event_id="EVT-20260424-005", object_id="OBJ-BR-002", video_id="VID-20260424-002",
        event_type="deformation", risk_level="medium", scene_type="day",
        event_time=datetime(2026, 4, 24, 8, 35, 40, tzinfo=timezone.utc),
        start_second=2140, end_second=2170,
        result_desc="连续帧中桥面边缘曲率异常，轮廓偏移 14px，桥端挠度接近阈值，需人工复核。",
        review_status="pending",
    ),
    EventRecord(
        event_id="EVT-20260424-006", object_id="OBJ-TN-001", video_id="VID-20260424-004",
        event_type="tunnel_anomaly", risk_level="medium", scene_type="day",
        event_time=datetime(2026, 4, 24, 9, 12, 30, tzinfo=timezone.utc),
        start_second=750, end_second=800,
        result_desc="CO 指数抬升 15%，照度下降 22%，视频烟雾特征与环境监测数据同时出现异常。",
        review_status="pending",
    ),
    EventRecord(
        event_id="EVT-20260425-001", object_id="OBJ-BR-003", video_id="VID-20260425-001",
        event_type="fire", risk_level="high", scene_type="night",
        event_time=datetime(2026, 4, 25, 19, 22, 5, tzinfo=timezone.utc),
        start_second=1325, end_second=1358,
        result_desc="夜间场景检测到异常热源，温度急剧上升，烟雾特征明显，判定为桥面火灾高风险事件。",
        review_status="pending",
    ),
    EventRecord(
        event_id="EVT-20260425-002", object_id="OBJ-BR-003", video_id="VID-20260425-001",
        event_type="congestion", risk_level="low", scene_type="night",
        event_time=datetime(2026, 4, 25, 19, 40, 18, tzinfo=timezone.utc),
        start_second=2418, end_second=2450,
        result_desc="车流速度下降但未达到高风险阈值，低风险事件，建议持续观察。",
        review_status="reviewed",
        review_remark="已确认为节假日返程高峰正常拥堵，非事故导致。",
    ),
]

MODELS = [
    ModelVersion(model_id="MDL-BRIDGE-V1.0", model_name="普通桥梁风险识别模型V1.0", model_type="bridge",
                 model_version="V1.0", status="active",
                 publish_time=datetime(2026, 4, 1, tzinfo=timezone.utc),
                 remark="一期基线模型，支持坍塌/变形/积压/火灾四类识别"),
    ModelVersion(model_id="MDL-SHIP-V0.1", model_name="船撞融合预警原型V0.1", model_type="ship_collision",
                 model_version="V0.1", status="inactive",
                 remark="原型验证模型，需进一步训练"),
    ModelVersion(model_id="MDL-TUNNEL-V0.1", model_name="隧道融合预警原型V0.1", model_type="tunnel",
                 model_version="V0.1", status="inactive",
                 remark="原型验证模型，需进一步训练"),
]

FUSION_RESULTS = [
    FusionResult(
        fusion_id="FUS-20260424-001", object_id="OBJ-BR-LARGE-001",
        related_event_id="EVT-20260424-003", fusion_type="ship_collision",
        score=72.5, risk_level="medium",
        rule_desc="船只接近桥墩区域，位移数据出现轻微波动，振动值升高。综合评分 72.5，判定中风险。",
        fusion_time=datetime(2026, 4, 24, 6, 46, 0, tzinfo=timezone.utc),
    ),
]

MONITORING_DATA = [
    # 位移监测
    MonitoringData(object_id="OBJ-BR-LARGE-001", data_type="displacement",
                   data_time=datetime(2026, 4, 24, 6, 40, 0, tzinfo=timezone.utc), data_value=0.02),
    MonitoringData(object_id="OBJ-BR-LARGE-001", data_type="displacement",
                   data_time=datetime(2026, 4, 24, 6, 45, 0, tzinfo=timezone.utc), data_value=0.05),
    MonitoringData(object_id="OBJ-BR-LARGE-001", data_type="displacement",
                   data_time=datetime(2026, 4, 24, 6, 50, 0, tzinfo=timezone.utc), data_value=0.03),
    # 振动监测
    MonitoringData(object_id="OBJ-BR-LARGE-001", data_type="vibration",
                   data_time=datetime(2026, 4, 24, 6, 40, 0, tzinfo=timezone.utc), data_value=0.8),
    MonitoringData(object_id="OBJ-BR-LARGE-001", data_type="vibration",
                   data_time=datetime(2026, 4, 24, 6, 45, 0, tzinfo=timezone.utc), data_value=1.2),
    MonitoringData(object_id="OBJ-BR-LARGE-001", data_type="vibration",
                   data_time=datetime(2026, 4, 24, 6, 50, 0, tzinfo=timezone.utc), data_value=0.9),
    # 水位监测
    MonitoringData(object_id="OBJ-BR-LARGE-001", data_type="water_level",
                   data_time=datetime(2026, 4, 24, 6, 45, 0, tzinfo=timezone.utc), data_value=15.3),
    # 隧道环境监测
    MonitoringData(object_id="OBJ-TN-001", data_type="co",
                   data_time=datetime(2026, 4, 24, 9, 10, 0, tzinfo=timezone.utc), data_value=42.0),
    MonitoringData(object_id="OBJ-TN-001", data_type="co",
                   data_time=datetime(2026, 4, 24, 9, 12, 0, tzinfo=timezone.utc), data_value=51.0),
    MonitoringData(object_id="OBJ-TN-001", data_type="lux",
                   data_time=datetime(2026, 4, 24, 9, 10, 0, tzinfo=timezone.utc), data_value=156.0),
]


# ──────────────────────────────────────────────
#  Seed runner
# ──────────────────────────────────────────────

async def seed_database() -> None:
    """Populate database with initial seed data."""
    logger.info("Starting database seeding...")

    async with async_session_factory() as session:
        # Check if already seeded
        from sqlalchemy import select, func
        count_result = await session.execute(select(func.count(ObjectInfo.object_id)))
        existing_count = count_result.scalar() or 0
        if existing_count > 0:
            logger.info("Database already seeded, skipping.")
            return

        # Insert in dependency order
        session.add_all(OBJECTS)
        await session.flush()

        session.add_all(VIDEOS)
        await session.flush()

        session.add_all(EVENTS)
        await session.flush()

        session.add_all(MODELS)
        await session.flush()

        session.add_all(FUSION_RESULTS)
        await session.flush()

        session.add_all(MONITORING_DATA)
        await session.commit()

        logger.info(f"Seeded {len(OBJECTS)} objects, {len(VIDEOS)} videos, {len(EVENTS)} events, "
                    f"{len(MODELS)} models, {len(FUSION_RESULTS)} fusion results, "
                    f"{len(MONITORING_DATA)} monitoring data points.")


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    await seed_database()


if __name__ == "__main__":
    asyncio.run(main())
