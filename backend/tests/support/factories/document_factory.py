"""
Document factory for creating test documents.

Uses faker to generate unique test data and supports overrides for explicit test intent.
"""
import uuid
from typing import Optional
from faker import Faker

from app.models.document import Document

fake = Faker()


class DocumentFactory:
    """Factory for creating Document test data."""

    @staticmethod
    def create_document(
        session,
        overrides: Optional[dict] = None,
    ) -> Document:
        """
        Create a Document instance with sensible defaults.

        Args:
            session: Database session for persisting the document
            overrides: Dictionary of field overrides

        Returns:
            Document instance (not yet committed to database)
        """
        if overrides is None:
            overrides = {}

        # Generate default content based on size
        content_size = overrides.get("content_size", "small")  # small, medium, large
        if content_size == "small":
            content = fake.text(max_nb_chars=1000)  # ~1 page
        elif content_size == "medium":
            content = fake.text(max_nb_chars=10000)  # ~10 pages
        elif content_size == "large":
            content = fake.text(max_nb_chars=50000)  # ~50 pages
        else:
            content = fake.text(max_nb_chars=1000)

        # Use provided content or generate default
        content = overrides.get("content", content)

        # Calculate file size from content
        file_size = len(content.encode("utf-8"))

        # Build document data
        document_data = {
            "content": content,
            "file_name": overrides.get("file_name", f"{fake.file_name(extension='txt')}"),
            "file_size": overrides.get("file_size", file_size),
            "source_language": overrides.get("source_language", "en"),
            "user_id": overrides.get("user_id"),
            "session_id": overrides.get("session_id", str(uuid.uuid4())),
        }

        # Create document instance
        document = Document(**document_data)
        session.add(document)
        return document

    @staticmethod
    def create_document_dict(overrides: Optional[dict] = None) -> dict:
        """
        Create a dictionary representing a document (for API testing).

        Args:
            overrides: Dictionary of field overrides

        Returns:
            Dictionary with document data
        """
        if overrides is None:
            overrides = {}

        content = overrides.get("content", fake.text(max_nb_chars=1000))
        file_size = len(content.encode("utf-8"))

        return {
            "content": content,
            "file_name": overrides.get("file_name", f"{fake.file_name(extension='txt')}"),
            "file_size": overrides.get("file_size", file_size),
            "source_language": overrides.get("source_language", "en"),
            "session_id": overrides.get("session_id", str(uuid.uuid4())),
        }

