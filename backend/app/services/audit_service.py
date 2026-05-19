"""
Service layer for Audit Logging (操作审计日志).
"""

import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.system_log import SystemLog
from app.utils.pagination import PaginationParams

logger = logging.getLogger(__name__)


class AuditService:
    """Business logic for recording and querying audit logs."""

    @staticmethod
    async def record(
        db: AsyncSession,
        log_type: str,
        log_content: str,
        log_level: str = "info",
        user_id: Optional[str] = None,
        operator_name: Optional[str] = None,
        related_id: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> SystemLog:
        """Record an audit log entry."""
        entry = SystemLog(
            log_type=log_type,
            log_level=log_level,
            log_content=log_content,
            user_id=user_id,
            operator_name=operator_name,
            related_id=related_id,
            ip_address=ip_address,
        )
        db.add(entry)
        await db.flush()
        return entry

    @staticmethod
    async def list_logs(
        db: AsyncSession,
        pagination: PaginationParams,
        log_type: Optional[str] = None,
        log_level: Optional[str] = None,
        user_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> tuple[list[dict], int]:
        """Query audit logs with filters."""
        query = select(SystemLog)
        count_query = select(func.count()).select_from(SystemLog)

        if log_type:
            query = query.where(SystemLog.log_type == log_type)
            count_query = count_query.where(SystemLog.log_type == log_type)
        if log_level:
            query = query.where(SystemLog.log_level == log_level)
            count_query = count_query.where(SystemLog.log_level == log_level)
        if user_id:
            query = query.where(SystemLog.user_id == user_id)
            count_query = count_query.where(SystemLog.user_id == user_id)
        if start_time:
            dt = datetime.fromisoformat(start_time)
            query = query.where(SystemLog.created_time >= dt)
            count_query = count_query.where(SystemLog.created_time >= dt)
        if end_time:
            dt = datetime.fromisoformat(end_time)
            query = query.where(SystemLog.created_time <= dt)
            count_query = count_query.where(SystemLog.created_time <= dt)

        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(SystemLog.created_time.desc())
        query = query.offset(pagination.offset).limit(pagination.limit)
        result = await db.execute(query)
        logs = result.scalars().all()

        return [AuditService._to_dict(log) for log in logs], total

    @staticmethod
    def _to_dict(log: SystemLog) -> dict:
        return {
            "log_id": log.log_id,
            "log_type": log.log_type,
            "log_level": log.log_level,
            "log_content": log.log_content,
            "user_id": log.user_id,
            "operator_name": log.operator_name,
            "related_id": log.related_id,
            "ip_address": log.ip_address,
            "created_time": log.created_time.isoformat() if log.created_time else None,
        }
