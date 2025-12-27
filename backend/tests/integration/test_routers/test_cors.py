"""
CORS configuration integration tests.

Tests that CORS headers are correctly set and unauthorized origins are rejected.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
async def client():
    """FastAPI test client fixture."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_cors_headers_present(client: AsyncClient):
    """Test CORS headers are present in responses."""
    response = await client.get(
        "/health",
        headers={"Origin": "http://localhost:3000"}
    )
    
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert "access-control-allow-credentials" in response.headers
    assert response.headers["access-control-allow-credentials"] == "true"


@pytest.mark.asyncio
async def test_cors_authorized_origin_allowed(client: AsyncClient):
    """Test authorized origin (http://localhost:3000) is allowed."""
    response = await client.get(
        "/health",
        headers={"Origin": "http://localhost:3000"}
    )
    
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


@pytest.mark.asyncio
async def test_cors_unauthorized_origin_rejected(client: AsyncClient):
    """Test unauthorized origins are rejected."""
    # Note: FastAPI CORS middleware will still allow the request but won't set
    # access-control-allow-origin for unauthorized origins
    response = await client.get(
        "/health",
        headers={"Origin": "http://malicious.com"}
    )
    
    assert response.status_code == 200
    # Unauthorized origin should not have access-control-allow-origin header
    # or it should be different from the request origin
    if "access-control-allow-origin" in response.headers:
        assert response.headers["access-control-allow-origin"] != "http://malicious.com"


@pytest.mark.asyncio
async def test_cors_preflight_options_request(client: AsyncClient):
    """Test CORS preflight (OPTIONS) requests work correctly."""
    response = await client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        }
    )
    
    assert response.status_code == 200
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-credentials" in response.headers
    assert response.headers["access-control-allow-credentials"] == "true"


@pytest.mark.asyncio
async def test_cors_allow_credentials_header(client: AsyncClient):
    """Test allow-credentials header is set correctly."""
    response = await client.get(
        "/health",
        headers={"Origin": "http://localhost:3000"}
    )
    
    assert response.status_code == 200
    assert response.headers["access-control-allow-credentials"] == "true"


@pytest.mark.asyncio
async def test_cors_different_http_methods(client: AsyncClient):
    """Test CORS works with different HTTP methods."""
    # Test GET
    response = await client.get(
        "/health",
        headers={"Origin": "http://localhost:3000"}
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    
    # Test POST (if endpoint existed)
    # For now, we'll test that OPTIONS preflight works for POST
    response = await client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST"
        }
    )
    assert response.status_code == 200
    assert "access-control-allow-methods" in response.headers

