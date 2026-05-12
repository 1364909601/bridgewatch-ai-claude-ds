"""
Authentication middleware: validates JWT from Authorization header.

Usage in router:
    from app.middleware.auth import get_current_user, require_role
    @router.get("/events")
    async def list_events(..., current_user: dict = Depends(get_current_user)):
        ...
"""

from typing import Optional

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.auth_service import AuthService
from app.utils.exceptions import ForbiddenException, UnauthorizedException


async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Validate the JWT from the Authorization header and return the current user.
    Raises 401 if the token is missing or invalid.
    """
    if not authorization:
        raise UnauthorizedException("缺少认证令牌")

    if not authorization.startswith("Bearer "):
        raise UnauthorizedException("认证令牌格式无效")

    token = authorization[7:]  # Strip "Bearer "
    payload = AuthService.decode_access_token(token)

    user_id = payload.get("user_id")
    if not user_id:
        raise UnauthorizedException("认证令牌无效")

    user = await AuthService.get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise UnauthorizedException("用户不存在或已被禁用")

    return {
        "user_id": user.user_id,
        "username": user.username,
        "display_name": user.display_name,
        "role": user.role,
    }


async def get_optional_user(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
) -> Optional[dict]:
    """
    Like get_current_user, but returns None instead of raising 401
    when no valid token is provided. Use for endpoints that work
    both with and without authentication.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization[7:]
    try:
        payload = AuthService.decode_access_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            return None
        user = await AuthService.get_user_by_id(db, user_id)
        if not user or not user.is_active:
            return None
        return {
            "user_id": user.user_id,
            "username": user.username,
            "display_name": user.display_name,
            "role": user.role,
        }
    except Exception:
        return None


def require_role(required_role: str):
    """
    Factory for role-checking dependency.

    Usage:
        @router.get("/admin-only")
        async def admin_endpoint(current_user: dict = Depends(require_role("admin"))):
            ...
    """
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        if current_user["role"] != required_role and current_user["role"] != "admin":
            raise ForbiddenException(f"需要 {required_role} 角色权限")
        return current_user

    return role_checker
