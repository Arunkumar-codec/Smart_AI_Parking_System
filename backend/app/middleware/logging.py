import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from backend.app.core.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        correlation_id = getattr(request.state, "correlation_id", "N/A")

        logger.info(
            "Started %s %s",
            request.method,
            request.url.path,
            extra={"correlation_id": correlation_id},
        )

        response = await call_next(request)

        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "Completed %s %s status=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
            extra={"correlation_id": correlation_id},
        )
        return response
