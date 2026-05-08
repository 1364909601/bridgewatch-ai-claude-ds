"""
Seed script for BridgeWatch AI backend development database.

Usage:
    python -m app.seed.seed_data

Requires a running PostgreSQL database with the schema already created.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_factory
from app.models.object_info import ObjectInfo
from app.models.video_info import VideoInfo
from app.models.event_record import EventRecord
from app.models.model_version import ModelVersion
from app.models.inference_task import InferenceTask
from app.models.monitoring_data import MonitoringData
from app.models.fusion_result import FusionResult
from app.utils.id_generator import generate_object_id, generate_video_id, generate_event_id, generate_model_id, generate_task_id, generate_fusion_id


async def seed_objects(db: AsyncSession):
    objects = [
        ObjectInfo(object_id=generate_object_id(), object_name="长江大桥", object_type="bridge", location_desc="长江流域主干道"),
        ObjectInfo(object_id=generate_object_id(), object_name="黄河大桥", object_type="bridge", location_desc="黄河流域主干道"),
        ObjectInfo(object_id=generate_object_id(), object_name="跨海大桥", object_type="bridge", location_desc="东部沿海跨海通道"),
        ObjectInfo(object_id=generate_object_id(), object_name="南山隧道", object_type="tunnel", location_desc="南部山区高速公路"),
        ObjectInfo(object_id=generate_object_id(), object_name="穿山隧道", object_type="tunnel", location_desc="西部山区高速公路"),
    ]
    for obj in objects:
        existing = await db.execute(select(ObjectInfo).where(ObjectInfo.object_name == obj.object_name))
        if not existing.scalar_one_or_none():
            db.add(obj)
    await db.commit()
    # Re-fetch to get generated IDs
    result = await db.execute(select(ObjectInfo))
    return {o.object_name: o for o in result.scalars().all()}


async def seed_videos(db: AsyncSession, obj_map: dict[str, ObjectInfo]):
    base_time = datetime.utcnow() - timedelta(days=7)
    videos_data = [
        (obj_map["长江大桥"], "长江大桥-日常巡检-01", base_time, 1800, "day"),
        (obj_map["长江大桥"], "长江大桥-日常巡检-02", base_time + timedelta(days=1), 3600, "day"),
        (obj_map["长江大桥"], "长江大桥-夜间巡检-01", base_time + timedelta(days=2), 1800, "night"),
        (obj_map["黄河大桥"], "黄河大桥-日常巡检-01", base_time + timedelta(days=1), 1200, "day"),
        (obj_map["黄河大桥"], "黄河大桥-雨雾巡检-01", base_time + timedelta(days=3), 900, "rain_fog"),
        (obj_map["跨海大桥"], "跨海大桥-日常巡检-01", base_time + timedelta(days=2), 2400, "day"),
        (obj_map["南山隧道"], "南山隧道-日常巡检-01", base_time + timedelta(days=1), 600, "day"),
        (obj_map["穿山隧道"], "穿山隧道-日常巡检-01", base_time + timedelta(days=2), 900, "night"),
    ]
    videos = []
    for obj, name, capture_time, duration, scene in videos_data:
        existing = await db.execute(select(VideoInfo).where(VideoInfo.video_name == name))
        if existing.scalar_one_or_none():
            continue
        vid = VideoInfo(
            video_id=generate_video_id(),
            object_id=obj.object_id,
            video_name=name,
            file_url=f"/files/videos/{name}.mp4",
            capture_time=capture_time,
            duration_seconds=duration,
            resolution="1920x1080",
            scene_type=scene,
            preprocess_status="done",
        )
        db.add(vid)
        videos.append(vid)
    await db.commit()
    result = await db.execute(select(VideoInfo))
    return {v.video_name: v for v in result.scalars().all()}


async def seed_events(db: AsyncSession, obj_map: dict[str, ObjectInfo], vid_map: dict[str, VideoInfo]):
    bridge_nj = obj_map["长江大桥"]
    bridge_hh = obj_map["黄河大桥"]
    vid_1 = vid_map.get("长江大桥-日常巡检-01")
    vid_2 = vid_map.get("长江大桥-日常巡检-02")
    vid_3 = vid_map.get("黄河大桥-日常巡检-01")
    vid_4 = vid_map.get("黄河大桥-雨雾巡检-01")

    if not all([vid_1, vid_2, vid_3, vid_4]):
        print("Warning: Some videos not found, skipping event seeding")
        return

    base_time = datetime.utcnow() - timedelta(days=6)
    events_data = [
        (bridge_nj, vid_1, "collapse", "high", "day", base_time, 120, 180, None, "检测到桥梁中部结构异常位移"),
        (bridge_nj, vid_1, "deformation", "medium", "day", base_time + timedelta(hours=2), 300, 420, None, "桥面出现不均匀沉降迹象"),
        (bridge_nj, vid_2, "congestion", "medium", "day", base_time + timedelta(days=1), 30, 600, None, "车辆拥堵长度超过阈值"),
        (bridge_nj, vid_2, "fire", "high", "day", base_time + timedelta(days=1, hours=1), 450, 510, None, "桥面中部检测到明火"),
        (bridge_nj, vid_3, "congestion", "low", "day", base_time + timedelta(days=2), 60, 300, None, "车流量较大"),
        (bridge_hh, vid_3, "deformation", "low", "day", base_time + timedelta(days=2, hours=3), 200, 280, None, "轻微结构变形"),
        (bridge_hh, vid_4, "collapse", "high", "rain_fog", base_time + timedelta(days=3), 50, 150, None, "雨雾天气下检测到疑似结构异常"),
        (bridge_hh, vid_4, "fire", "medium", "rain_fog", base_time + timedelta(days=3, hours=2), 180, 240, None, "桥面边缘检测到烟雾"),
    ]
    for obj, vid, etype, risk, scene, etime, start, end, thumb, desc in events_data:
        existing = await db.execute(
            select(EventRecord).where(
                EventRecord.video_id == vid.video_id,
                EventRecord.event_type == etype,
                EventRecord.start_second == start,
            )
        )
        if existing.scalar_one_or_none():
            continue
        event = EventRecord(
            event_id=generate_event_id(),
            object_id=obj.object_id,
            video_id=vid.video_id,
            event_type=etype,
            risk_level=risk,
            scene_type=scene,
            event_time=etime,
            start_second=start,
            end_second=end,
            result_desc=desc,
            review_status="pending",
        )
        db.add(event)
    await db.commit()


async def seed_models(db: AsyncSession):
    models_data = [
        ("BridgeWatch Vision", "vision", "1.4.2", "active"),
        ("Ship Collision Fusion", "fusion", "0.8.6", "active"),
        ("Tunnel Guard", "tunnel", "0.6.1", "inactive"),
    ]
    for name, mtype, version, status in models_data:
        existing = await db.execute(
            select(ModelVersion).where(
                ModelVersion.model_name == name,
                ModelVersion.model_version == version,
            )
        )
        if existing.scalar_one_or_none():
            continue
        model = ModelVersion(
            model_id=generate_model_id(),
            model_name=name,
            model_type=mtype,
            model_version=version,
            status=status,
            publish_time=datetime.utcnow() - timedelta(days=30),
        )
        db.add(model)
    await db.commit()


async def seed_tasks(db: AsyncSession, vid_map: dict[str, VideoInfo]):
    model_result = await db.execute(select(ModelVersion))
    models = model_result.scalars().all()
    if not models or not vid_map:
        return

    vid = list(vid_map.values())[0]
    model = models[0]

    existing = await db.execute(
        select(InferenceTask).where(InferenceTask.video_id == vid.video_id)
    )
    if existing.scalar_one_or_none():
        return

    tasks = [
        InferenceTask(
            task_id=generate_task_id(),
            video_id=vid.video_id,
            model_id=model.model_id,
            task_name=f"推理任务-{model.model_name}",
            task_status="success",
            start_time=datetime.utcnow() - timedelta(days=5),
            end_time=datetime.utcnow() - timedelta(days=5) + timedelta(hours=2),
            result_summary="检测到 2 个事件",
        ),
        InferenceTask(
            task_id=generate_task_id(),
            video_id=vid.video_id,
            model_id=model.model_id,
            task_name=f"批量推理-{model.model_name}",
            task_status="running",
            start_time=datetime.utcnow() - timedelta(hours=1),
        ),
    ]
    for t in tasks:
        db.add(t)
    await db.commit()


async def seed_monitoring_data(db: AsyncSession, obj_map: dict[str, ObjectInfo]):
    bridge = obj_map["跨海大桥"]
    base_time = datetime.utcnow() - timedelta(hours=24)

    existing = await db.execute(
        select(MonitoringData).where(
            MonitoringData.object_id == bridge.object_id,
            MonitoringData.data_type == "vibration",
        ).limit(1)
    )
    if existing.scalar_one_or_none():
        return

    data_types = ["displacement", "vibration", "water_level", "strain"]
    for dt_type in data_types:
        for i in range(24):
            md = MonitoringData(
                object_id=bridge.object_id,
                data_type=dt_type,
                data_time=base_time + timedelta(hours=i),
                data_value=10 + (i * 0.5) + (i % 3) * 2,
            )
            db.add(md)
    await db.commit()


async def seed_fusion(db: AsyncSession, obj_map: dict[str, ObjectInfo]):
    bridge = obj_map["跨海大桥"]
    existing = await db.execute(
        select(FusionResult).where(
            FusionResult.object_id == bridge.object_id,
        ).limit(1)
    )
    if existing.scalar_one_or_none():
        return

    for i in range(3):
        fusion = FusionResult(
            fusion_id=generate_fusion_id(),
            object_id=bridge.object_id,
            fusion_type="ship_collision",
            score=85.0 - i * 10,
            risk_level="high" if i == 0 else "medium",
            rule_desc=f"船撞融合评分: AIS接近度 + 视频距离 + 应变峰值 + 振动能量",
            fusion_time=datetime.utcnow() - timedelta(hours=i * 8),
        )
        db.add(fusion)
    await db.commit()


async def main():
    print("Seeding database...")
    async with async_session_factory() as session:
        obj_map = await seed_objects(session)
        print(f"  Objects: {len(obj_map)}")
        vid_map = await seed_videos(session, obj_map)
        print(f"  Videos: {len(vid_map)}")
        await seed_events(session, obj_map, vid_map)
        print(f"  Events: seeded")
        await seed_models(session)
        print(f"  Models: seeded")
        await seed_tasks(session, vid_map)
        print(f"  Tasks: seeded")
        await seed_monitoring_data(session, obj_map)
        print(f"  Monitoring data: seeded")
        await seed_fusion(session, obj_map)
        print(f"  Fusion results: seeded")
    print("Seed complete!")


if __name__ == "__main__":
    asyncio.run(main())
