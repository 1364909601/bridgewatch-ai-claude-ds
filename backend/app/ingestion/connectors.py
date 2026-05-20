"""
Data source connectors — simulate reading from external systems.

In production, each ``collect()`` method would call an external API,
read from a message queue, or poll a device.
"""

import logging
import random
from datetime import datetime, timedelta, timezone
from typing import Any

logger = logging.getLogger(__name__)


class ShmSensorConnector:
    """
    Simulate a Structural Health Monitoring (SHM) sensor.

    Real implementation: read from vibration/displacement/strain gauges
    installed on bridge structures via Modbus TCP or REST API.
    """

    def __init__(self, object_id: str, base_url: str = ""):
        self.object_id = object_id
        self.base_url = base_url

    async def collect(self) -> list[dict[str, Any]]:
        """Read current sensor values."""
        now = datetime.now(timezone.utc)
        return [
            {"object_id": self.object_id, "data_type": "displacement",
             "data_value": round(random.uniform(0.01, 0.08), 4), "data_time": now.isoformat()},
            {"object_id": self.object_id, "data_type": "vibration",
             "data_value": round(random.uniform(0.3, 2.1), 3), "data_time": now.isoformat()},
            {"object_id": self.object_id, "data_type": "strain",
             "data_value": round(random.uniform(100, 250), 1), "data_time": now.isoformat()},
        ]


class AisReceiver:
    """
    Simulate an AIS (Automatic Identification System) receiver.

    Real implementation: connect to AIS base station or maritime data API
    (e.g., MarineTraffic, exactEarth) to receive ship positions, speed, heading.
    """

    def __init__(self, object_id: str, api_key: str = ""):
        self.object_id = object_id
        self.api_key = api_key

    async def collect(self) -> list[dict[str, Any]]:
        """Get latest AIS data for ships near the bridge."""
        now = datetime.now(timezone.utc)
        # Simulate 1-3 ships in the area
        ships = random.randint(1, 3)
        results = []
        for _ in range(ships):
            results.append({
                "object_id": self.object_id,
                "data_type": "ais",
                "data_value": round(random.uniform(1.5, 5.0), 2),  # distance (km)
                "data_time": now.isoformat(),
                "ext_json": {
                    "ship_name": random.choice(["长明货轮", "东方之星", "海丰联航", "中远海运"]),
                    "speed": round(random.uniform(6, 18), 1),
                    "heading": random.randint(0, 359),
                    "cargo_type": random.choice(["container", "bulk", "tanker"]),
                },
            })
        return results


class TunnelEnvironmentSensor:
    """
    Simulate tunnel environment sensors.

    Real implementation: read from CO detectors, visibility sensors,
    illuminance meters, and traffic counters installed in the tunnel.
    """

    def __init__(self, object_id: str):
        self.object_id = object_id

    async def collect(self) -> list[dict[str, Any]]:
        """Read tunnel environment data."""
        now = datetime.now(timezone.utc)
        return [
            {"object_id": self.object_id, "data_type": "co",
             "data_value": round(random.uniform(25, 65), 1), "data_time": now.isoformat()},
            {"object_id": self.object_id, "data_type": "lux",
             "data_value": round(random.uniform(80, 200), 1), "data_time": now.isoformat()},
            {"object_id": self.object_id, "data_type": "traffic",
             "data_value": random.randint(300, 1800), "data_time": now.isoformat()},
        ]


class VideoStreamIngester:
    """
    Simulate video stream ingestion.

    Real implementation: connect to RTSP/RTMP video streams from UAVs
    or fixed cameras, run preprocessing (frame extraction, scene detection),
    then trigger inference tasks.
    """

    def __init__(self, object_id: str, stream_url: str = ""):
        self.object_id = object_id
        self.stream_url = stream_url

    async def collect(self) -> dict[str, Any]:
        """Simulate a video capture event with metadata."""
        now = datetime.now(timezone.utc)
        return {
            "object_id": self.object_id,
            "video_name": f"stream_{self.object_id}_{now.strftime('%Y%m%d_%H%M%S')}",
            "file_url": self.stream_url or f"/videos/live/{self.object_id}.m3u8",
            "capture_time": now.isoformat(),
            "duration_seconds": random.choice([300, 600, 1800]),
            "resolution": "1920x1080",
            "scene_type": random.choice(["day", "night", "rain_fog"]),
            "preprocess_status": "pending",
        }
