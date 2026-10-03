import time
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import settings
from backend.app.core.exceptions import DatabaseError
from backend.app.schemas.common import DatabaseHealthResponse, HealthCheckResponse
from backend.app.services.base import BaseService


class HealthService(BaseService):
    async def check_liveness(self) -> HealthCheckResponse:
        return HealthCheckResponse(
            status="healthy",
            environment=settings.APP_ENV,
            version="1.0.0",
            timestamp=datetime.now(timezone.utc),
        )

    async def check_readiness(self) -> DatabaseHealthResponse:
        if self.db is None:
            raise DatabaseError("Database session is unavailable.")

        start = time.perf_counter()

        try:
            result = await self.db.execute(
                text(
                    "SELECT extname "
                    "FROM pg_extension "
                    "WHERE extname IN ('vector', 'btree_gist') "
                    "ORDER BY extname"
                )
            )
            extensions = list(result.scalars().all())
            latency_ms = (time.perf_counter() - start) * 1000

            return DatabaseHealthResponse(
                status="healthy",
                database="postgresql",
                latency_ms=round(latency_ms, 2),
                extensions=extensions,
                timestamp=datetime.now(timezone.utc),
            )
        except Exception as exc:
            raise DatabaseError("Database readiness check failed.") from exc
