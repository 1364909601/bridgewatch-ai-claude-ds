import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start = time.time()

        response: Response = await call_next(request)
        elapsed = time.time() - start

        # Attach request ID header
        response.headers["X-Request-ID"] = request_id

        # Log request info
        print(f"[{request_id}] {request.method} {request.url.path} - {response.status_code} ({elapsed:.3f}s)")

        return response
