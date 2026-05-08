from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class InferenceTask(Base):
    __tablename__ = "inference_task"

    task_id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="任务ID")
    video_id: Mapped[str] = mapped_column(String(64), ForeignKey("video_info.video_id"), nullable=False, comment="关联视频ID")
    model_id: Mapped[str] = mapped_column(String(64), ForeignKey("model_version.model_id"), nullable=False, comment="关联模型ID")
    task_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="任务名称")
    task_status: Mapped[str] = mapped_column(String(32), nullable=False, default="queued", comment="任务状态: queued/running/success/failed")
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="开始时间")
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, comment="结束时间")
    result_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="结果摘要")
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="错误信息")
    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # Relationships
    video_info: Mapped["VideoInfo"] = relationship(back_populates="inference_tasks")
    model_version: Mapped["ModelVersion"] = relationship(back_populates="inference_tasks")

    def __repr__(self) -> str:
        return f"<InferenceTask {self.task_id}: {self.task_name} [{self.task_status}]>"
