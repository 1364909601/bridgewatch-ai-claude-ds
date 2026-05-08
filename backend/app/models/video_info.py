from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class VideoInfo(Base):
    __tablename__ = "video_info"

    video_id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="视频ID")
    object_id: Mapped[str] = mapped_column(String(64), ForeignKey("object_info.object_id"), nullable=False, comment="所属对象ID")
    video_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="视频名称")
    file_url: Mapped[str] = mapped_column(String(500), nullable=False, comment="文件路径/URL")
    capture_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment="拍摄时间")
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="视频时长(秒)")
    resolution: Mapped[Optional[str]] = mapped_column(String(32), nullable=True, comment="分辨率")
    scene_type: Mapped[Optional[str]] = mapped_column(String(32), nullable=True, comment="场景: day/night/rain_fog")
    preprocess_status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending", comment="预处理状态: pending/done/failed")
    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # Relationships
    object_info: Mapped["ObjectInfo"] = relationship(back_populates="videos")
    events: Mapped[list["EventRecord"]] = relationship(back_populates="video_info")
    inference_tasks: Mapped[list["InferenceTask"]] = relationship(back_populates="video_info")

    def __repr__(self) -> str:
        return f"<VideoInfo {self.video_id}: {self.video_name}>"
