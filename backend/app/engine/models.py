"""
Data models for the detection engine layer.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DetectionResult:
    """A single event detected by a detector on one video."""
    event_type: str       # "collapse" | "deformation" | "congestion" | "fire"
    confidence: float     # 0.0 to 1.0
    risk_level: str       # "low" | "medium" | "high"
    start_second: int     # start time in the video
    end_second: int       # end time in the video
    result_desc: str      # Chinese description string
    scene_type: Optional[str] = None  # inherited from video metadata


@dataclass
class DetectionSummary:
    """Aggregated output of running all detectors on one video."""
    task_id: str
    video_id: str
    object_id: str
    scene_type: Optional[str]
    video_duration: int
    results: list[DetectionResult] = field(default_factory=list)
    is_success: bool = True
    error_message: Optional[str] = None
