import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint_accepts_correlation_id(
    async_client: AsyncClient,
):
    correlation_id = "phase4-test-correlation-id"
    response = await async_client.get(
        "/api/v1/health",
        headers={"X-Correlation-ID": correlation_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == correlation_id
