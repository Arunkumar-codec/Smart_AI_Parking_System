import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_liveness_endpoint(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_db_readiness_endpoint(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health/db")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "postgresql"
    assert "vector" in data["extensions"]
    assert "btree_gist" in data["extensions"]
