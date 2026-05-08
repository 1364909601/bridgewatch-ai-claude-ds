from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ObjectInfo(Base):
    __tablename__ = "object_info"

    object_id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="对象ID")
    object_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="对象名称")
    object_type: Mapped[str] = mapped_column(String(32), nullable=False, comment="对象类型: bridge/tunnel")
    location_desc: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="位置描述")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active", comment="状态: active/inactive")
    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # Relationships
    videos: Mapped[list["VideoInfo"]] = relationship(back_populates="object_info", cascade="all, delete-orphan")
    events: Mapped[list["EventRecord"]] = relationship(back_populates="object_info")
    monitoring_data: Mapped[list["MonitoringData"]] = relationship(back_populates="object_info")
    fusion_results: Mapped[list["FusionResult"]] = relationship(back_populates="object_info")

    def __repr__(self) -> str:
        return f"<ObjectInfo {self.object_id}: {self.object_name}>"
