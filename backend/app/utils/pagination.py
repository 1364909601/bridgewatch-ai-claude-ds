from datetime import datetime
from math import ceil

from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class PaginationParams:
    def __init__(self, page_no: int = 1, page_size: int = 20):
        self.page_no = max(1, page_no)
        self.page_size = max(1, min(100, page_size))

    @property
    def offset(self) -> int:
        return (self.page_no - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    page_no: int
    page_size: int
    list: list[T]


def paginated_response(items: list[T], total: int, params: PaginationParams) -> PaginatedResponse[T]:
    return PaginatedResponse(
        total=total,
        page_no=params.page_no,
        page_size=params.page_size,
        list=items,
    )
