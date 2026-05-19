"""
Service layer for Alert notifications (告警通知).
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert_record import AlertRecord
from app.models.event_record import EventRecord
from app.utils.exceptions import NotFoundException, BadRequestException
from app.utils.id_generator import IDGenerator
from app.utils.pagination import PaginationParams

logger = logging.getLogger(__name__)


class AlertService:
    """Business logic for alert evaluation and management."""

    # ── Alert evaluation ──────────────────────────────────────────────

    @staticmethod
    def _generate_alert_id() -> str:
        return IDGenerator.generate_unique("ALERT")

    @staticmethod
    def _alert_for_event(event: EventRecord) -> Optional[AlertRecord]:
        """
        Evaluate whether an event should trigger an alert.
        Returns an AlertRecord (unsaved) or None.
        """
        alert_type = "new_high_risk_event"
        severity: str = "info"
        title: str = ""
        message: str = ""

        if event.risk_level == "high":
            severity = "critical"
            if event.event_type in ("collapse", "fire"):
                title = f"高风险事件: {event.event_type}"
                message = (
                    f"检测到 {event.event_type} 事件，风险等级为高，"
                    f"置信度评估已达高风险阈值，需立即复核处理。"
                )
            else:
                title = "高风险事件待复核"
                message = f"事件风险等级为高，需及时复核确认。"
        elif event.risk_level == "medium":
            severity = "warning"
            title = "中风险事件待关注"
            message = f"事件风险等级为中，建议安排复核。"
        else:
            # Low risk → info-level alert
            severity = "info"
            title = "低风险事件提示"
            message = f"事件风险等级为低，维持自动巡检。"
            return None  # Skip info-level alerts for now

        return AlertRecord(
            alert_id=AlertService._generate_alert_id(),
            related_event_id=event.event_id,
            alert_type=alert_type,
            severity=severity,
            title=title,
            message=message,
            status="unread",
        )

    @staticmethod
    async def evaluate_new_event(db: AsyncSession, event: EventRecord) -> Optional[AlertRecord]:
        """
        Evaluate and persist an alert for a newly created event.
        Returns the created AlertRecord, or None if no alert is needed.
        """
        alert = AlertService._alert_for_event(event)
        if alert is None:
            return None
        db.add(alert)
        await db.flush()
        logger.info("Alert %s generated for event %s (severity=%s)", alert.alert_id, event.event_id, alert.severity)
        return alert

    @staticmethod
    async def check_escalations(
        db: AsyncSession,
        high_risk_minutes: int = 30,
        medium_risk_minutes: int = 60,
    ) -> int:
        """
        Check for unacknowledged events that need escalation.
        Returns count of escalation alerts created.
        """
        now = datetime.now(timezone.utc)
        high_cutoff = now - timedelta(minutes=high_risk_minutes)
        medium_cutoff = now - timedelta(minutes=medium_risk_minutes)
        created = 0

        # High-risk unacknowledged events older than high_risk_minutes
        result = await db.execute(
            select(EventRecord).where(
                EventRecord.risk_level == "high",
                EventRecord.review_status != "reviewed",
                EventRecord.created_time < high_cutoff,
            )
        )
        for event in result.scalars().all():
            # Check if escalation alert already exists for this event
            existing = await db.execute(
                select(AlertRecord).where(
                    AlertRecord.related_event_id == event.event_id,
                    AlertRecord.alert_type == "escalation",
                )
            )
            if existing.scalar_one_or_none() is None:
                alert = AlertRecord(
                    alert_id=AlertService._generate_alert_id(),
                    related_event_id=event.event_id,
                    alert_type="escalation",
                    severity="critical",
                    title="高风险事件超时未复核",
                    message=(
                        f"事件 {event.event_id} 创建已超过 {high_risk_minutes} 分钟仍未复核，"
                        f"系统自动升级告警等级。"
                    ),
                    status="unread",
                )
                db.add(alert)
                created += 1

        # Medium-risk unacknowledged events older than medium_risk_minutes
        result = await db.execute(
            select(EventRecord).where(
                EventRecord.risk_level == "medium",
                EventRecord.review_status != "reviewed",
                EventRecord.created_time < medium_cutoff,
            )
        )
        for event in result.scalars().all():
            existing = await db.execute(
                select(AlertRecord).where(
                    AlertRecord.related_event_id == event.event_id,
                    AlertRecord.alert_type == "escalation",
                )
            )
            if existing.scalar_one_or_none() is None:
                alert = AlertRecord(
                    alert_id=AlertService._generate_alert_id(),
                    related_event_id=event.event_id,
                    alert_type="escalation",
                    severity="warning",
                    title="中风险事件超时未复核",
                    message=(
                        f"事件 {event.event_id} 创建已超过 {medium_risk_minutes} 分钟仍未复核，"
                        f"建议尽快处理。"
                    ),
                    status="unread",
                )
                db.add(alert)
                created += 1

        if created > 0:
            await db.flush()
            logger.info("Created %d escalation alerts", created)

        return created

    # ── CRUD ──────────────────────────────────────────────────────────

    @staticmethod
    async def get_active_count(db: AsyncSession) -> dict:
        """Get count of active (unacknowledged) alerts — includes both unread and read statuses."""
        result = await db.execute(
            select(func.count()).select_from(AlertRecord).where(
                AlertRecord.status.in_(["unread", "read"])
            )
        )
        count = result.scalar() or 0
        return {"count": count}

    @staticmethod
    async def list_alerts(
        db: AsyncSession,
        pagination: PaginationParams,
        status: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> tuple[list[dict], int]:
        """List alerts with optional filtering."""
        query = select(AlertRecord)
        count_query = select(func.count()).select_from(AlertRecord)

        if status:
            query = query.where(AlertRecord.status == status)
            count_query = count_query.where(AlertRecord.status == status)
        if severity:
            query = query.where(AlertRecord.severity == severity)
            count_query = count_query.where(AlertRecord.severity == severity)

        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        query = query.order_by(AlertRecord.created_time.desc())
        query = query.offset(pagination.offset).limit(pagination.limit)
        result = await db.execute(query)
        alerts = result.scalars().all()

        return [AlertService._to_dict(a) for a in alerts], total

    @staticmethod
    async def acknowledge_alert(db: AsyncSession, alert_id: str) -> dict:
        """Mark a single alert as acknowledged."""
        result = await db.execute(
            select(AlertRecord).where(AlertRecord.alert_id == alert_id)
        )
        alert = result.scalar_one_or_none()
        if not alert:
            raise NotFoundException(f"告警 {alert_id} 不存在")
        if alert.status == "acknowledged":
            raise BadRequestException(f"告警 {alert_id} 已被确认")

        alert.status = "acknowledged"
        await db.commit()
        await db.refresh(alert)
        return AlertService._to_dict(alert)

    @staticmethod
    async def batch_acknowledge(db: AsyncSession, alert_ids: list[str]) -> dict:
        """Mark multiple alerts as acknowledged."""
        result = await db.execute(
            select(AlertRecord).where(AlertRecord.alert_id.in_(alert_ids))
        )
        alerts = result.scalars().all()
        found_ids = {a.alert_id for a in alerts}
        missing = [aid for aid in alert_ids if aid not in found_ids]
        for alert in alerts:
            alert.status = "acknowledged"
        await db.commit()
        return {"acknowledged": len(alerts), "not_found": missing}

    # ── Helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _to_dict(alert: AlertRecord) -> dict:
        return {
            "alert_id": alert.alert_id,
            "related_event_id": alert.related_event_id,
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "title": alert.title,
            "message": alert.message,
            "status": alert.status,
            "created_time": alert.created_time.isoformat() if alert.created_time else None,
        }
