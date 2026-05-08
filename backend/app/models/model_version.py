from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ModelVersion(Base):
    __tablename__ = "model_version"

    model_id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="模型ID")
    model_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="模型名称")
    model_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="模型类型")
    model_version: Mapped[str] = mapped_column(String(64), nullable=False, comment="版本号")
    file_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="模型文件URL")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active", comment="状态: active/inactive/deprecated")
    publish_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="发布时间")
    remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="备注")
    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # Relationships
    inference_tasks: Mapped[list["InferenceTask"]] = relationship(back_populates="model_version")

    def __repr__(self) -> str:
        return f"<ModelVersion {self.model_id}: {self.model_name} v{self.model_version}>"
