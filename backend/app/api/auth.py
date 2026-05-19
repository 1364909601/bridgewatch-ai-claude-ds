"""
API endpoints for Authentication (用户认证).
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.schemas.auth import LoginRequest
from app.services.audit_service import AuditService
from app.services.auth_service import AuthService
from app.utils.exceptions import UnauthorizedException
from app.utils.response import success_response

router = APIRouter()


@router.post("/login")
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """用户登录，返回 JWT token"""
    user = await AuthService.authenticate_user(db, body.username, body.password)
    if not user:
        raise UnauthorizedException("用户名或密码错误")

    token = AuthService.create_access_token({
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role,
    })

    # Audit log
    await AuditService.record(
        db, log_type="login",
        log_content=f"用户 {user.username}({user.display_name}) 登录系统",
        user_id=user.user_id, operator_name=user.display_name,
    )
    await db.commit()

    return success_response({
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username,
        "display_name": user.display_name,
        "role": user.role,
    })


@router.get("/me")
async def get_me(
    current_user: dict = Depends(get_current_user),
):
    """获取当前登录用户信息"""
    return success_response(current_user)


@router.post("/seed")
async def seed_users(
    db: AsyncSession = Depends(get_db),
):
    """创建默认用户（仅 DEBUG 模式可用）"""
    from app.config import settings
    if not settings.DEBUG:
        return success_response({"created": 0, "message": "非 DEBUG 模式，跳过"})

    created = await AuthService.seed_users(db)
    await db.commit()
    return success_response({
        "created": created,
        "message": f"创建了 {created} 个默认用户" if created else "用户已存在，跳过",
    })
