"""
User model for authentication and authorization.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(64), primary_key=True, comment="用户ID")
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, comment="登录用户名")
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False, comment="密码哈希(bcrypt)")
    display_name: Mapped[str] = mapped_column(String(100), nullable=False, default="", comment="显示名称")
    role: Mapped[str] = mapped_column(String(32), nullable=False, default="viewer", comment="角色: admin/operator/viewer")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, comment="是否启用")
    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), comment="创建时间",
    )

    def __repr__(self) -> str:
        return f"<User {self.username} role={self.role}>"
