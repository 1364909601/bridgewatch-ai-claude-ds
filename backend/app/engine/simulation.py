"""
Deterministic pseudo-random simulation utilities.

All functions produce reproducible results given the same (video_id, event_type) pair.
This ensures that the same video always generates the same detection outcomes.
"""

import hashlib
import math
from typing import Optional


def _digest_fraction(key: str) -> float:
    """Deterministic float in [0, 1) derived from an MD5 hash of `key`."""
    h = hashlib.md5(key.encode()).digest()
    return int.from_bytes(h[:4], "big") / 0xFFFFFFFF


def should_detect(video_id: str, event_type: str, base_prob: float) -> bool:
    """Deterministically decide whether an event fires for a given video."""
    return _digest_fraction(f"detect:{video_id}:{event_type}") < base_prob


def sample_confidence(
    video_id: str,
    event_type: str,
    mean: float = 0.75,
    std: float = 0.08,
) -> float:
    """
    Sample a confidence value from a clamped normal distribution.
    Uses Box-Muller transform seeded by a hash of (video_id, event_type).
    """
    u1 = _digest_fraction(f"conf_u1:{video_id}:{event_type}")
    u2 = _digest_fraction(f"conf_u2:{video_id}:{event_type}")
    # Box-Muller transform
    epsilon = 1e-10
    z = math.sqrt(-2.0 * math.log(max(u1, epsilon))) * math.cos(2.0 * math.pi * u2)
    return max(0.0, min(1.0, mean + z * std))


def risk_level_from_confidence(confidence: float, event_type: str) -> str:
    """
    Map a confidence score to a risk level.
    Collapse is more sensitive (high at >= 0.75).
    """
    thresholds = {
        "collapse": (0.75, 0.60),
        "deformation": (0.80, 0.65),
        "congestion": (0.85, 0.70),
        "fire": (0.80, 0.65),
    }
    high_th, med_th = thresholds.get(event_type, (0.85, 0.65))
    if confidence >= high_th:
        return "high"
    if confidence >= med_th:
        return "medium"
    return "low"


def pick_time_window(
    duration: int,
    region: str,
    video_id: str,
    event_type: str,
) -> tuple[int, int]:
    """
    Pick (start_second, end_second) within video duration [0, duration).

    ``region`` controls where in the timeline the event tends to appear:
      - "early"  → first 30 %
      - "middle" → 25 %–65 %
      - "late"   → last 35 %
      - "any"    → 5 %–95 %
    """
    dur = max(duration, 30)  # minimum 30 s window

    region_ranges = {
        "early": (0.00, 0.30),
        "middle": (0.25, 0.65),
        "late": (0.65, 1.00),
        "any": (0.05, 0.95),
    }
    lo, hi = region_ranges.get(region, (0.05, 0.95))

    frac = _digest_fraction(f"tw_pos:{video_id}:{event_type}")
    center = lo + frac * (hi - lo)

    # Window width: 5 %–20 % of video length
    width_frac = 0.05 + _digest_fraction(f"tw_wid:{video_id}:{event_type}") * 0.15
    half = int(dur * width_frac / 2)
    mid = int(dur * center)

    start_sec = max(0, mid - half)
    end_sec = min(dur - 1, mid + half)
    if end_sec - start_sec < 10:
        end_sec = min(dur - 1, start_sec + 10)

    return start_sec, end_sec


def select_description(descriptions: list[str], video_id: str, event_type: str) -> str:
    """Deterministically pick one description from a list."""
    idx = int(_digest_fraction(f"desc:{video_id}:{event_type}") * len(descriptions))
    return descriptions[idx]
