from datetime import datetime, timezone
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: Optional[T] = None
    timestamp: str = ""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def success_response(data: Any = None, message: str = "success") -> ApiResponse:
    return ApiResponse(code=0, message=message, data=data, timestamp=_now())


def error_response(code: int, message: str) -> ApiResponse:
    return ApiResponse(code=code, message=message, data=None, timestamp=_now())
