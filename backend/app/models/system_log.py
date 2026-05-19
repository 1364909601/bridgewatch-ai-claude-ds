from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SystemLog(Base):
    __tablename__ = "system_log"

    log_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="日志ID")
    log_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="日志类型: login/event_review/user_mgmt/task/alert/system")
    related_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, comment="关联对象ID")
    user_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, comment="操作用户ID")
    operator_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="操作人姓名")
    log_level: Mapped[str] = mapped_column(String(32), nullable=False, default="info", comment="日志级别: info/warn/error")
    log_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="日志内容")
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="请求IP")
    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    def __repr__(self) -> str:
        return f"<SystemLog {self.log_id}: [{self.log_level}] {self.log_type}>"
