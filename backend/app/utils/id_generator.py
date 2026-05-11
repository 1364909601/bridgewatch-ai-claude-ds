from datetime import datetime


class IDGenerator:
    """Generate IDs in format: {PREFIX}-{YYYYMMDD}-{NNN}"""

    _counters: dict[str, int] = {}

    @classmethod
    def generate(cls, prefix: str = "ID") -> str:
        today = datetime.now().strftime("%Y%m%d")
        key = f"{prefix}-{today}"
        cls._counters[key] = cls._counters.get(key, 0) + 1
        return f"{prefix}-{today}-{cls._counters[key]:03d}"

    @classmethod
    def generate_unique(cls, prefix: str = "ID") -> str:
        """Generate an ID with current timestamp to avoid cross-process collisions."""
        import secrets
        now = datetime.now()
        return f"{prefix}-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}-{secrets.token_hex(2)}"


def generate_event_id() -> str:
    return IDGenerator.generate_unique("EVT")


def generate_video_id() -> str:
    return IDGenerator.generate("VID")


def generate_task_id() -> str:
    return IDGenerator.generate_unique("TASK")


def generate_model_id() -> str:
    return IDGenerator.generate("MOD")


def generate_object_id() -> str:
    return IDGenerator.generate("OBJ")


def generate_fusion_id() -> str:
    return IDGenerator.generate("FUS")


def generate_log_id() -> int:
    """system_log uses BIGSERIAL auto-increment, no prefix needed"""
    return 0
