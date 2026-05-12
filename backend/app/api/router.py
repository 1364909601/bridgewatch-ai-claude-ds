from fastapi import APIRouter, Depends

from app.api.health import router as health_router
from app.api.objects import router as objects_router
from app.api.dicts import router as dicts_router
from app.api.dashboard import router as dashboard_router
from app.api.events import router as events_router
from app.api.videos import router as videos_router
from app.api.tasks import router as tasks_router
from app.api.topics import router as topics_router
from app.api.alerts import router as alerts_router
from app.api.auth import router as auth_router
from app.api.monitoring import router as monitoring_router
from app.middleware.auth import get_current_user

api_router = APIRouter()

# Public routes (no auth required)
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Protected API routes (auth required)
protected_routes = [
    (objects_router, "/objects", "Objects"),
    (dicts_router, "/dicts", "Dicts"),
    (dashboard_router, "/dashboard", "Dashboard"),
    (events_router, "/events", "Events"),
    (videos_router, "/videos", "Videos"),
    (tasks_router, "/tasks", "Tasks"),
    (topics_router, "/topics", "Topics"),
    (alerts_router, "/alerts", "Alerts"),
    (monitoring_router, "/monitoring", "Monitoring"),
]
for router, prefix, tag in protected_routes:
    api_router.include_router(router, prefix=prefix, tags=[tag], dependencies=[Depends(get_current_user)])
