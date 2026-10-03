from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.deps import get_db_session
from backend.app.schemas.common import DatabaseHealthResponse, HealthCheckResponse
from backend.app.schemas.error import ErrorResponse
from backend.app.services.health_service import HealthService

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Application liveness check",
)
async def liveness_check() -> HealthCheckResponse:
    service = HealthService(db=None)
    return await service.check_liveness()


@router.get(
    "/health/db",
    response_model=DatabaseHealthResponse,
    status_code=status.HTTP_200_OK,
    responses={500: {"model": ErrorResponse}},
    summary="Database readiness check",
)
async def readiness_check(
    db: AsyncSession = Depends(get_db_session),
) -> DatabaseHealthResponse:
    service = HealthService(db=db)
    return await service.check_readiness()
