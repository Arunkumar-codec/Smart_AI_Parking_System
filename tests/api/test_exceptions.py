import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_unknown_route_returns_404(async_client: AsyncClient):
    response = await async_client.get("/api/v1/non_existent_path")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_correlation_id_header(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health")
    assert "X-Correlation-ID" in response.headers
    assert response.headers["X-Correlation-ID"]
