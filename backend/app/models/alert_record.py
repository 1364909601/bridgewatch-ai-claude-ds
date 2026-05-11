"""
Alert notification record model.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AlertRecord(Base):
    __tablename__ = "alert_record"

    alert_id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="告警ID")
    related_event_id: Mapped[Optional[str]] = mapped_column(
        String(64), ForeignKey("event_record.event_id"), nullable=True,
        comment="关联事件ID",
    )
    alert_type: Mapped[str] = mapped_column(
        String(32), nullable=False, default="new_high_risk_event",
        comment="告警类型: new_high_risk_event / threshold_exceeded / escalation",
    )
    severity: Mapped[str] = mapped_column(
        String(16), nullable=False, default="warning",
        comment="严重等级: info / warning / critical",
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="告警标题")
    message: Mapped[str] = mapped_column(Text, nullable=True, default="", comment="告警详情")
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="unread",
        comment="状态: unread / read / acknowledged / escalated",
    )
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="创建时间",
    )

    def __repr__(self) -> str:
        return f"<AlertRecord {self.alert_id} severity={self.severity} status={self.status}>"
