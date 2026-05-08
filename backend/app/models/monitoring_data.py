from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, func
from sqlalchemy import Numeric as DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MonitoringData(Base):
    __tablename__ = "monitoring_data"

    data_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="数据ID")
    object_id: Mapped[str] = mapped_column(String(64), ForeignKey("object_info.object_id"), nullable=False, comment="所属对象ID")
    data_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="数据类型: displacement/vibration/water_level/ais/co/lux/traffic")
    data_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="数据时间")
    data_value: Mapped[float] = mapped_column(DECIMAL(18, 4), nullable=False, comment="数值")
    ext_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, comment="扩展属性")
    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # Relationships
    object_info: Mapped["ObjectInfo"] = relationship(back_populates="monitoring_data")

    def __repr__(self) -> str:
        return f"<MonitoringData {self.data_id}: {self.object_id}/{self.data_type} = {self.data_value}>"
