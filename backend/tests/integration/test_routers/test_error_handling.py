"""
Error handling integration tests.

Tests that global exception handler catches exceptions and returns structured error responses.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import HTTPException
from app.main import app


@pytest.fixture
async def client():
    """FastAPI test client fixture."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_error_response_format(client: AsyncClient):
    """Test error response format matches specification."""
    # Test with non-existent endpoint (404)
    response = await client.get("/nonexistent-endpoint")
    
    assert response.status_code == 404
    data = response.json()
    
    # Check error response structure - should use structured format
    assert "error" in data
    assert "code" in data["error"]
    assert "message" in data["error"]
    assert "timestamp" in data["error"]
    assert "request_id" in data["error"]
    assert data["error"]["code"] == "HTTP_404"


@pytest.mark.asyncio
async def test_error_response_has_request_id(client: AsyncClient):
    """Test error response includes request_id."""
    response = await client.get("/nonexistent-endpoint")
    
    assert response.status_code == 404
    data = response.json()
    
    # Error handler should always provide request_id in structured format
    assert "error" in data
    assert "request_id" in data["error"]
    assert isinstance(data["error"]["request_id"], str)
    assert len(data["error"]["request_id"]) > 0


@pytest.mark.asyncio
async def test_error_response_has_timestamp(client: AsyncClient):
    """Test error response includes timestamp."""
    response = await client.get("/nonexistent-endpoint")
    
    assert response.status_code == 404
    data = response.json()
    
    # Error handler should always provide timestamp in structured format
    assert "error" in data
    assert "timestamp" in data["error"]
    timestamp = data["error"]["timestamp"]
    assert "T" in timestamp  # ISO 8601 format


@pytest.mark.asyncio
async def test_error_response_no_sensitive_data(client: AsyncClient):
    """Test error response does not contain sensitive information."""
    response = await client.get("/nonexistent-endpoint")
    
    assert response.status_code == 404
    data = response.json()
    response_text = str(data)
    
    # Verify no API keys in error response
    assert "OPENAI_API_KEY" not in response_text
    assert "sk-" not in response_text  # OpenAI API key prefix
    
    # Verify no stack traces in error response
    assert "Traceback" not in response_text
    assert "File \"" not in response_text
    assert ".py" not in response_text or ".py" not in response_text.lower()

