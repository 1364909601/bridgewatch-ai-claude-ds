from enum import StrEnum


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SceneType(StrEnum):
    DAY = "day"
    NIGHT = "night"
    RAIN_FOG = "rain_fog"


class ReviewStatus(StrEnum):
    PENDING = "pending"
    REVIEWED = "reviewed"


class TaskStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class ObjectType(StrEnum):
    BRIDGE = "bridge"
    TUNNEL = "tunnel"


class EventType(StrEnum):
    COLLAPSE = "collapse"
    DEFORMATION = "deformation"
    CONGESTION = "congestion"
    FIRE = "fire"
    SHIP_COLLISION = "ship_collision"


class FusionType(StrEnum):
    SHIP_COLLISION = "ship_collision"
    TUNNEL = "tunnel"


class ModelStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPRECATED = "deprecated"


class DataType(StrEnum):
    DISPLACEMENT = "displacement"
    VIBRATION = "vibration"
    WATER_LEVEL = "water_level"
    STRAIN = "strain"
    AIS = "ais"
    CO = "co"
    LUX = "lux"
    TRAFFIC = "traffic"
    TEMPERATURE = "temperature"
    WIND_SPEED = "wind_speed"
