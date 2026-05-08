"""
Shared Pydantic models for pagination and common response patterns.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination query parameters validated by FastAPI."""
    page_no: int = 1
    page_size: int = 20

    @property
    def offset(self) -> int:
        return (self.page_no - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated list response."""
    total: int
    page_no: int
    page_size: int
    list: list[T]
