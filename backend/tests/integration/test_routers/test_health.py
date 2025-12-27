"""
Health check endpoint integration tests.
"""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """
    Test health check endpoint returns 200 and correct JSON structure.
    """
    response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    # Verify timestamp is ISO 8601 format
    assert "T" in data["timestamp"]

