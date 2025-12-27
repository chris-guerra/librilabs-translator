"""
API helper functions for testing.

Pure functions for making API requests and validating responses.
"""
from typing import Optional, Dict, Any
from httpx import AsyncClient


async def create_document_via_api(
    client: AsyncClient,
    file_content: str,
    file_name: str = "test.txt",
    source_language: str = "en",
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a document via API endpoint.

    Args:
        client: FastAPI test client
        file_content: Content of the file to upload
        file_name: Name of the file
        source_language: Source language code
        session_id: Optional session ID

    Returns:
        Response JSON data
    """
    headers = {}
    if session_id:
        headers["X-Session-Id"] = session_id

    files = {"file": (file_name, file_content.encode("utf-8"), "text/plain")}
    data = {"source_language": source_language}

    response = await client.post(
        "/api/v1/documents/upload",
        files=files,
        data=data,
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


async def get_document_via_api(
    client: AsyncClient,
    document_id: str,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get a document via API endpoint.

    Args:
        client: FastAPI test client
        document_id: Document ID
        session_id: Optional session ID

    Returns:
        Response JSON data
    """
    headers = {}
    if session_id:
        headers["X-Session-Id"] = session_id

    response = await client.get(
        f"/api/v1/documents/{document_id}",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


async def create_translation_via_api(
    client: AsyncClient,
    document_id: str,
    target_language: str = "es",
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a translation via API endpoint.

    Args:
        client: FastAPI test client
        document_id: Document ID
        target_language: Target language code
        session_id: Optional session ID

    Returns:
        Response JSON data
    """
    headers = {"Content-Type": "application/json"}
    if session_id:
        headers["X-Session-Id"] = session_id

    response = await client.post(
        "/api/v1/translations/create",
        json={
            "document_id": document_id,
            "target_language": target_language,
        },
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


async def get_translation_status_via_api(
    client: AsyncClient,
    translation_id: str,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Get translation status via API endpoint.

    Args:
        client: FastAPI test client
        translation_id: Translation ID
        session_id: Optional session ID

    Returns:
        Response JSON data
    """
    headers = {}
    if session_id:
        headers["X-Session-Id"] = session_id

    response = await client.get(
        f"/api/v1/translations/{translation_id}/status",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()

