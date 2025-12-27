"""
Example integration test demonstrating factory usage.

This test shows how to use factories and fixtures for test data creation.
"""
import pytest
from httpx import AsyncClient

from tests.support.factories import DocumentFactory


@pytest.mark.asyncio
async def test_create_document_with_factory(client: AsyncClient, test_db_session, document_factory):
    """Test document creation using factory."""
    # Create document using factory
    document = document_factory.create_document(
        test_db_session,
        overrides={
            "content": "Test document content",
            "file_name": "test.txt",
            "source_language": "en",
        },
    )
    await test_db_session.commit()

    # Verify document was created
    assert document.id is not None
    assert document.content == "Test document content"
    assert document.file_name == "test.txt"
    assert document.source_language == "en"


@pytest.mark.asyncio
async def test_create_document_via_api(client: AsyncClient, unique_session_id):
    """Test document creation via API endpoint."""
    from tests.support.helpers.api_helpers import create_document_via_api

    # Create document via API
    document = await create_document_via_api(
        client,
        file_content="Test content",
        file_name="test.txt",
        source_language="en",
        session_id=unique_session_id,
    )

    # Verify response
    assert document["id"] is not None
    assert document["file_name"] == "test.txt"
    assert document["source_language"] == "en"


@pytest.mark.asyncio
async def test_get_document_via_api(client: AsyncClient, test_db_session, unique_session_id):
    """Test getting document via API endpoint."""
    from tests.support.helpers.api_helpers import create_document_via_api, get_document_via_api

    # Create document first
    created = await create_document_via_api(
        client,
        file_content="Test content",
        file_name="test.txt",
        source_language="en",
        session_id=unique_session_id,
    )

    # Get document
    fetched = await get_document_via_api(
        client,
        document_id=created["id"],
        session_id=unique_session_id,
    )

    # Verify
    assert fetched["id"] == created["id"]
    assert fetched["file_name"] == "test.txt"

