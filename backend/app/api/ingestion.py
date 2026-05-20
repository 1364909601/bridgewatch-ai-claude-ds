"""
API endpoints for Data Ingestion (数据接入).
"""

from fastapi import APIRouter, Depends, Query

from app.database import get_db
from app.ingestion.pipeline import IngestionPipeline
from app.middleware.auth import require_role
from app.utils.response import success_response

router = APIRouter()


@router.post("/trigger")
async def trigger_ingestion(
    bridge_id: str = Query("OBJ-20260508-001"),
    large_bridge_id: str = Query("OBJ-20260508-003"),
    tunnel_id: str = Query("OBJ-20260508-004"),
    current_user: dict = Depends(require_role("admin")),
):
    """手动触发一次数据接入（从模拟源采集最新数据并入库）"""
    pipeline = IngestionPipeline()
    counts = await pipeline.run_once(
        bridge_id=bridge_id,
        large_bridge_id=large_bridge_id,
        tunnel_id=tunnel_id,
    )
    return success_response(counts)
