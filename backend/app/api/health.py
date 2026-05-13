from fastapi import APIRouter
from starlette.responses import Response

from app.config import settings
from app.monitoring.metrics import get_metrics
from app.utils.response import success_response

router = APIRouter()


@router.get("/health")
async def health_check():
    return success_response({
        "status": "ok",
        "version": settings.APP_VERSION,
        "app_name": settings.APP_NAME,
    })


@router.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint — returns text/plain format."""
    data = get_metrics()
    return Response(content=data, media_type="text/plain; charset=utf-8")
