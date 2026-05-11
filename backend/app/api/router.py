from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.objects import router as objects_router
from app.api.dicts import router as dicts_router
from app.api.dashboard import router as dashboard_router
from app.api.events import router as events_router
from app.api.videos import router as videos_router
from app.api.tasks import router as tasks_router
from app.api.topics import router as topics_router
from app.api.alerts import router as alerts_router

api_router = APIRouter()

# Health check (no auth)
api_router.include_router(health_router, tags=["Health"])

# Protected API routes
api_router.include_router(objects_router, prefix="/objects", tags=["Objects"])
api_router.include_router(dicts_router, prefix="/dicts", tags=["Dicts"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(events_router, prefix="/events", tags=["Events"])
api_router.include_router(videos_router, prefix="/videos", tags=["Videos"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(topics_router, prefix="/topics", tags=["Topics"])
api_router.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])
