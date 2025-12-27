"""
CORS production configuration tests.

Tests that CORS can be configured via environment variables for production.
"""
import os
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch
from importlib import reload


@pytest.fixture
async def client_production_origins():
    """FastAPI test client with production CORS origins."""
    # Set environment variable before importing
    original_origins = os.environ.get("ALLOWED_ORIGINS")
    os.environ["ALLOWED_ORIGINS"] = "https://app.librilabs.com,https://www.librilabs.com"
    
    try:
        # Reload the module to pick up new environment variable
        import app.main
        reload(app.main)
        app = app.main.app
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac
    finally:
        # Restore original environment
        if original_origins:
            os.environ["ALLOWED_ORIGINS"] = original_origins
        elif "ALLOWED_ORIGINS" in os.environ:
            del os.environ["ALLOWED_ORIGINS"]
        # Reload module to restore default
        import app.main
        reload(app.main)


@pytest.mark.asyncio
async def test_cors_production_origins_from_env(client_production_origins: AsyncClient):
    """Test CORS can be configured via ALLOWED_ORIGINS environment variable."""
    # Test with first production origin
    response = await client_production_origins.get(
        "/health",
        headers={"Origin": "https://app.librilabs.com"}
    )
    
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "https://app.librilabs.com"
    
    # Test with second production origin
    response2 = await client_production_origins.get(
        "/health",
        headers={"Origin": "https://www.librilabs.com"}
    )
    
    assert response2.status_code == 200
    assert response2.headers["access-control-allow-origin"] == "https://www.librilabs.com"


@pytest.mark.asyncio
async def test_cors_production_unauthorized_origin_rejected(client_production_origins: AsyncClient):
    """Test unauthorized origins are rejected in production configuration."""
    response = await client_production_origins.get(
        "/health",
        headers={"Origin": "http://malicious.com"}
    )
    
    assert response.status_code == 200
    # Unauthorized origin should not have access-control-allow-origin header
    # or it should be different from the request origin
    if "access-control-allow-origin" in response.headers:
        assert response.headers["access-control-allow-origin"] != "http://malicious.com"

