"""
BridgeWatch AI Detection Engine.

Provides simulation-based detection for four ordinary-bridge event types:
collapse, deformation, congestion, and fire.
"""

from app.engine.models import DetectionResult, DetectionSummary
from app.engine.detector import (
    CollapseDetector,
    DeformationDetector,
    CongestionDetector,
    FireDetector,
    run_detection_pipeline,
)
from app.engine.worker import InferenceWorker
from app.engine.batch import create_batch_tasks

__all__ = [
    "DetectionResult",
    "DetectionSummary",
    "CollapseDetector",
    "DeformationDetector",
    "CongestionDetector",
    "FireDetector",
    "run_detection_pipeline",
    "InferenceWorker",
    "create_batch_tasks",
]
