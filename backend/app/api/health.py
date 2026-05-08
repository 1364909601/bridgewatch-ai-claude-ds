from fastapi import APIRouter

from app.config import settings
from app.utils.response import success_response

router = APIRouter()


@router.get("/health")
async def health_check():
    return success_response({
        "status": "ok",
        "version": settings.APP_VERSION,
        "app_name": settings.APP_NAME,
    })
