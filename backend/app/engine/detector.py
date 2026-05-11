"""
Detection simulators for the four ordinary-bridge event types.

Each detector implements ``detect(video, object_info) -> DetectionResult | None``.
"""

import logging
from typing import Optional

from app.models.object_info import ObjectInfo
from app.models.video_info import VideoInfo
from app.engine.models import DetectionResult
from app.engine.simulation import (
    pick_time_window,
    risk_level_from_confidence,
    sample_confidence,
    select_description,
    should_detect,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------

class BaseDetector:
    """Base class with common detection logic."""

    event_type: str = ""
    descriptions: list[str] = []
    base_prob: float = 0.0
    scene_modifiers: dict[str, float] = {}
    duration_threshold: int = 0
    time_region: str = "any"
    conf_mean: float = 0.0

    def _adjusted_probability(self, video: VideoInfo) -> float:
        prob = self.base_prob
        if video.scene_type and video.scene_type in self.scene_modifiers:
            prob += self.scene_modifiers[video.scene_type]
        # Longer videos = more observation time = slightly higher chance
        dur = video.duration_seconds or 300
        if dur > 1800:
            prob += 0.05
        elif dur < 600:
            prob -= 0.05
        return max(0.0, min(1.0, prob))

    def detect(self, video: VideoInfo, object_info: ObjectInfo) -> Optional[DetectionResult]:
        """Return a DetectionResult if the event fires, else None."""
        if not video.video_id:
            return None
        dur = video.duration_seconds or 300
        if dur < self.duration_threshold:
            return None

        prob = self._adjusted_probability(video)
        if not should_detect(video.video_id, self.event_type, prob):
            return None

        confidence = sample_confidence(video.video_id, self.event_type, self.conf_mean)
        risk_level = risk_level_from_confidence(confidence, self.event_type)
        start_sec, end_sec = pick_time_window(dur, self.time_region, video.video_id, self.event_type)
        desc = select_description(self.descriptions, video.video_id, self.event_type)

        return DetectionResult(
            event_type=self.event_type,
            confidence=confidence,
            risk_level=risk_level,
            start_second=start_sec,
            end_second=end_sec,
            result_desc=desc,
            scene_type=video.scene_type,
        )


# ---------------------------------------------------------------------------
# Concrete detectors
# ---------------------------------------------------------------------------

class CollapseDetector(BaseDetector):
    """Bridge collapse / structural failure detection."""
    event_type = "collapse"
    base_prob = 0.15
    scene_modifiers = {"rain_fog": 0.12, "night": 0.05}
    duration_threshold = 300   # at least 5 min
    time_region = "late"       # structural issues appear later
    conf_mean = 0.75
    descriptions = [
        "检测到桥梁主体结构异常位移，疑似坍塌风险",
        "桥墩区域出现结构性裂缝扩展，存在坍塌隐患",
        "桥梁关键节点位移超限，坍塌风险等级升高",
        "检测到桥梁承重结构异常变形，需立即复核",
    ]


class DeformationDetector(BaseDetector):
    """Bridge deck deformation detection."""
    event_type = "deformation"
    base_prob = 0.25
    scene_modifiers = {"night": 0.08, "rain_fog": 0.05}
    duration_threshold = 120
    time_region = "middle"
    conf_mean = 0.70
    descriptions = [
        "桥面局部区域出现不均匀沉降变形",
        "检测到桥面线性位移异常，存在结构变形",
        "桥梁上部结构出现扭曲变形迹象",
        "桥面板接缝处检测到异常相对位移",
    ]


class CongestionDetector(BaseDetector):
    """Vehicle congestion / queue detection."""
    event_type = "congestion"
    base_prob = 0.40
    scene_modifiers = {"day": 0.15, "rain_fog": 0.08}
    duration_threshold = 60
    time_region = "early"
    conf_mean = 0.80
    descriptions = [
        "检测到车辆积压，排队长度超过预警阈值",
        "桥面交通流量饱和，车辆通行速度低于限值",
        "多车道同时出现车辆积压，拥堵等级较高",
        "检测到桥面车辆缓行，平均速度低于10km/h",
    ]


class FireDetector(BaseDetector):
    """Bridge deck fire / thermal anomaly detection."""
    event_type = "fire"
    base_prob = 0.10
    scene_modifiers = {"night": 0.12, "rain_fog": 0.05}
    duration_threshold = 60
    time_region = "any"
    conf_mean = 0.65
    descriptions = [
        "检测到桥面异常高温区域，疑似火灾",
        "桥面边缘检测到烟雾和热源，存在火灾风险",
        "红外热成像检测到局部温度骤升，疑似起火",
        "检测到桥梁附属设施过热，存在火灾隐患",
    ]


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def run_detection_pipeline(video: VideoInfo, object_info: ObjectInfo) -> list[DetectionResult]:
    """
    Run all four ordinary-bridge detectors on a video and return
    all (non-None) results sorted by start_second.
    """
    detectors = [
        CollapseDetector(),
        DeformationDetector(),
        CongestionDetector(),
        FireDetector(),
    ]
    results: list[DetectionResult] = []
    for det in detectors:
        try:
            result = det.detect(video, object_info)
            if result is not None:
                results.append(result)
        except Exception:
            logger.exception("Detector %s failed on video %s", det.event_type, video.video_id)
    results.sort(key=lambda r: r.start_second)
    return results
