# Service layer — business logic for all API domains
from app.services.object_service import ObjectService
from app.services.event_service import EventService
from app.services.video_service import VideoService
from app.services.task_service import TaskService
from app.services.dashboard_service import DashboardService
from app.services.topic_service import TopicService
from app.services.dict_service import DictService

__all__ = [
    "ObjectService",
    "EventService",
    "VideoService",
    "TaskService",
    "DashboardService",
    "TopicService",
    "DictService",
]
