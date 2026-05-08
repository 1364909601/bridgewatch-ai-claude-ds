from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy import Numeric as DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class FusionResult(Base):
    __tablename__ = "fusion_result"

    fusion_id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="融合结果ID")
    object_id: Mapped[str] = mapped_column(String(64), ForeignKey("object_info.object_id"), nullable=False, comment="所属对象ID")
    related_event_id: Mapped[Optional[str]] = mapped_column(String(64), ForeignKey("event_record.event_id"), nullable=True, comment="关联事件ID")
    fusion_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="融合类型: ship_collision/tunnel")
    score: Mapped[Optional[float]] = mapped_column(DECIMAL(8, 2), nullable=True, comment="融合评分")
    risk_level: Mapped[str] = mapped_column(String(32), nullable=False, default="low", comment="风险等级: low/medium/high")
    rule_desc: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="规则描述")
    fusion_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="融合时间")
    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # Relationships
    object_info: Mapped["ObjectInfo"] = relationship(back_populates="fusion_results")
    related_event: Mapped[Optional["EventRecord"]] = relationship(back_populates="fusion_results")

    def __repr__(self) -> str:
        return f"<FusionResult {self.fusion_id}: {self.fusion_type} score={self.score}>"
