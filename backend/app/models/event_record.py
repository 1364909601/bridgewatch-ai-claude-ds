from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EventRecord(Base):
    __tablename__ = "event_record"

    event_id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="事件ID")
    object_id: Mapped[str] = mapped_column(String(64), ForeignKey("object_info.object_id"), nullable=False, comment="所属对象ID")
    video_id: Mapped[str] = mapped_column(String(64), ForeignKey("video_info.video_id"), nullable=False, comment="关联视频ID")
    event_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="事件类型: collapse/deformation/congestion/fire")
    risk_level: Mapped[str] = mapped_column(String(32), nullable=False, default="low", comment="风险等级: low/medium/high")
    scene_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True, comment="场景: day/night/rain_fog")
    event_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="事件时间")
    start_second: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="事件开始秒数")
    end_second: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="事件结束秒数")
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="缩略图URL")
    clip_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="视频片段URL")
    result_desc: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="识别结果描述")
    review_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending", comment="复核状态: pending/reviewed")
    review_remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="复核备注")
    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # Relationships
    object_info: Mapped["ObjectInfo"] = relationship(back_populates="events")
    video_info: Mapped["VideoInfo"] = relationship(back_populates="events")
    fusion_results: Mapped[list["FusionResult"]] = relationship(back_populates="related_event")

    def __repr__(self) -> str:
        return f"<EventRecord {self.event_id}: {self.event_type}/{self.risk_level}>"
