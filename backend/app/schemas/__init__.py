# Pydantic schemas for request/response serialization and OpenAPI docs
from app.schemas.common import (
    PaginationParams,
    PaginatedResponse,
)
from app.schemas.objects import (
    ObjectQueryParams,
    ObjectResponse,
)
from app.schemas.events import (
    EventQueryParams,
    EventResponse,
    EventDetailResponse,
    EventReviewRequest,
    EventReviewResponse,
)
from app.schemas.videos import (
    VideoQueryParams,
    VideoResponse,
    VideoEventMarkResponse,
    VideoPlayUrlResponse,
)
from app.schemas.tasks import (
    TaskCreateRequest,
    TaskQueryParams,
    TaskResponse,
)
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    DashboardTrendPoint,
    DashboardDistributionItem,
)
from app.schemas.topics import (
    BridgeSummaryResponse,
    FusionResultResponse,
)
from app.schemas.dicts import DictItem

__all__ = [
    "PaginationParams",
    "PaginatedResponse",
    "ObjectQueryParams",
    "ObjectResponse",
    "EventQueryParams",
    "EventResponse",
    "EventDetailResponse",
    "EventReviewRequest",
    "EventReviewResponse",
    "VideoQueryParams",
    "VideoResponse",
    "VideoEventMarkResponse",
    "VideoPlayUrlResponse",
    "TaskCreateRequest",
    "TaskQueryParams",
    "TaskResponse",
    "DashboardSummaryResponse",
    "DashboardTrendPoint",
    "DashboardDistributionItem",
    "BridgeSummaryResponse",
    "FusionResultResponse",
    "DictItem",
]
