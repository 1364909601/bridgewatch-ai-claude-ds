import logging
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.utils.response import error_response

logger = logging.getLogger(__name__)


class AppException(Exception):
    def __init__(self, code: int, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code


class NotFoundException(AppException):
    def __init__(self, message: str = "资源不存在"):
        super().__init__(code=404, message=message, status_code=404)


class BadRequestException(AppException):
    def __init__(self, message: str = "参数错误"):
        super().__init__(code=400, message=message, status_code=400)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "未授权访问"):
        super().__init__(code=401, message=message, status_code=401)


class ForbiddenException(AppException):
    def __init__(self, message: str = "权限不足"):
        super().__init__(code=403, message=message, status_code=403)


async def app_exception_handler(request: Request, exc: AppException):
    logger.warning(f"App exception: {exc.message} (code={exc.code})")
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.code, exc.message).model_dump(),
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content=error_response(500, "服务器内部错误").model_dump(),
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
