"""
API endpoints for User Management (用户管理).
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user, require_role
from app.services.audit_service import AuditService
from app.models.user import User
from app.schemas.users import CreateUserRequest, UpdateUserRequest
from app.services.auth_service import AuthService
from app.utils.exceptions import BadRequestException, NotFoundException
from app.utils.id_generator import IDGenerator
from app.utils.pagination import PaginationParams
from app.utils.response import success_response

router = APIRouter()


@router.get("")
async def list_users(
    page_no: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("admin")),
):
    """获取用户列表（仅 admin）"""
    result = await db.execute(select(User).offset((page_no - 1) * page_size).limit(page_size))
    users = result.scalars().all()
    total_result = await db.execute(select(func.count()).select_from(User))
    total = total_result.scalar() or 0
    return success_response({
        "total": total,
        "page_no": page_no,
        "page_size": page_size,
        "list": [AuthService.user_to_dict(u) for u in users],
    })


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("admin")),
):
    """获取单个用户信息"""
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundException(f"用户 {user_id} 不存在")
    return success_response(AuthService.user_to_dict(user))


@router.post("")
async def create_user(
    body: CreateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("admin")),
):
    """创建新用户"""
    existing = await AuthService.get_user_by_username(db, body.username)
    if existing:
        raise BadRequestException(f"用户名 {body.username} 已存在")
    if body.role not in ("admin", "operator", "viewer"):
        raise BadRequestException("角色必须为 admin/operator/viewer")

    user = User(
        user_id=IDGenerator.generate("USR"),
        username=body.username,
        hashed_password=AuthService.hash_password(body.password),
        display_name=body.display_name,
        role=body.role,
        is_active=True,
    )
    db.add(user)
    await db.flush()
    await AuditService.record(
        db, log_type="user_mgmt",
        log_content=f"管理员 {current_user['username']} 创建用户 {body.username} (角色: {body.role})",
        user_id=current_user["user_id"], operator_name=current_user["display_name"],
        related_id=user.user_id,
    )
    await db.commit()
    await db.refresh(user)
    return success_response(AuthService.user_to_dict(user))


@router.put("/{user_id}")
async def update_user(
    user_id: str,
    body: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("admin")),
):
    """更新用户信息"""
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundException(f"用户 {user_id} 不存在")

    if body.username is not None:
        existing = await AuthService.get_user_by_username(db, body.username)
        if existing and existing.user_id != user_id:
            raise BadRequestException(f"用户名 {body.username} 已被使用")
        user.username = body.username
    if body.password is not None:
        user.hashed_password = AuthService.hash_password(body.password)
    if body.display_name is not None:
        user.display_name = body.display_name
    if body.role is not None:
        if body.role not in ("admin", "operator", "viewer"):
            raise BadRequestException("角色必须为 admin/operator/viewer")
        user.role = body.role
    if body.is_active is not None:
        user.is_active = body.is_active

    await db.flush()
    await AuditService.record(
        db, log_type="user_mgmt",
        log_content=f"管理员 {current_user['username']} 更新用户 {user.username}",
        user_id=current_user["user_id"], operator_name=current_user["display_name"],
        related_id=user_id,
    )
    await db.commit()
    await db.refresh(user)
    return success_response(AuthService.user_to_dict(user))


@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role("admin")),
):
    """删除用户"""
    if user_id == current_user["user_id"]:
        raise BadRequestException("不能删除自己")
    user = await db.get(User, user_id)
    if not user:
        raise NotFoundException(f"用户 {user_id} 不存在")
    await db.delete(user)
    await db.flush()
    await AuditService.record(
        db, log_type="user_mgmt",
        log_content=f"管理员 {current_user['username']} 删除用户 {user.username} (ID: {user_id})",
        user_id=current_user["user_id"], operator_name=current_user["display_name"],
        related_id=user_id,
    )
    await db.commit()
    return success_response({"deleted": user_id})
