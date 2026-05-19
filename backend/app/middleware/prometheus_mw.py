"""
Prometheus middleware — records HTTP request metrics.

Tracks request count (by method, endpoint, status) and request duration.
"""

import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.monitoring.metrics import HTTP_REQUESTS_TOTAL, HTTP_REQUEST_DURATION


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware that records HTTP request count and duration."""

    async def dispatch(self, request: Request, call_next):
        method = request.method
        # Use the route path template if available, fallback to URL path
        endpoint = request.scope.get("path", "/unknown")

        start = time.monotonic()
        response: Response | None = None
        try:
            response = await call_next(request)
            return response
        finally:
            duration = time.monotonic() - start
            status_code = response.status_code if response is not None else 500

            HTTP_REQUESTS_TOTAL.labels(
                method=method, endpoint=endpoint, status=str(status_code)
            ).inc()

            HTTP_REQUEST_DURATION.labels(
                method=method, endpoint=endpoint
            ).observe(duration)
