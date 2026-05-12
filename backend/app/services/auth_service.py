"""
Service layer for Authentication (用户认证).
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import User
from app.utils.exceptions import UnauthorizedException
from app.utils.id_generator import IDGenerator

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Business logic for user authentication and JWT management."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plain-text password."""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain-text password against a hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_access_token(token: str) -> dict:
        """Decode and validate a JWT token. Returns the payload dict."""
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError as e:
            raise UnauthorizedException(f"无效的认证令牌: {e}")

    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[User]:
        """Verify username/password and return the User if valid."""
        result = await db.execute(
            select(User).where(User.username == username, User.is_active == True)
        )
        user = result.scalar_one_or_none()
        if user is None:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
        """Get a user by their ID."""
        return await db.get(User, user_id)

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Get a user by username."""
        result = await db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def seed_users(db: AsyncSession) -> int:
        """Create default users for development. Returns count created."""
        from app.models.user import User

        default_users = [
            {"username": "admin", "password": "admin123", "display_name": "系统管理员", "role": "admin"},
            {"username": "operator", "password": "operator123", "display_name": "值班操作员", "role": "operator"},
            {"username": "viewer", "password": "viewer123", "display_name": "观察员", "role": "viewer"},
        ]

        created = 0
        for u in default_users:
            existing = await AuthService.get_user_by_username(db, u["username"])
            if existing:
                continue
            user = User(
                user_id=IDGenerator.generate("USR"),
                username=u["username"],
                hashed_password=AuthService.hash_password(u["password"]),
                display_name=u["display_name"],
                role=u["role"],
                is_active=True,
            )
            db.add(user)
            created += 1

        if created > 0:
            await db.flush()
            logger.info("Seeded %d default users: %s", created, [u["username"] for u in default_users])

        return created

    @staticmethod
    def user_to_dict(user: User) -> dict:
        """Convert a User ORM object to a safe dict (no password)."""
        return {
            "user_id": user.user_id,
            "username": user.username,
            "display_name": user.display_name,
            "role": user.role,
            "is_active": user.is_active,
            "created_time": user.created_time.isoformat() if user.created_time else None,
        }
