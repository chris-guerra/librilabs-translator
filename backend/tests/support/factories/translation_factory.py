"""
Translation factory for creating test translations.

Uses faker to generate unique test data and supports overrides for explicit test intent.
"""
import uuid
from typing import Optional, Dict, Any
from faker import Faker

from app.models.translation import Translation

fake = Faker()


class TranslationFactory:
    """Factory for creating Translation test data."""

    @staticmethod
    def create_translation(
        session,
        document_id: uuid.UUID,
        overrides: Optional[dict] = None,
    ) -> Translation:
        """
        Create a Translation instance with sensible defaults.

        Args:
            session: Database session for persisting the translation
            document_id: ID of the document being translated (required)
            overrides: Dictionary of field overrides

        Returns:
            Translation instance (not yet committed to database)
        """
        if overrides is None:
            overrides = {}

        # Generate translated content based on status
        status = overrides.get("status", "pending")
        if status == "completed":
            # Generate realistic translated content
            translated_content = overrides.get(
                "translated_content", fake.text(max_nb_chars=5000)
            )
            progress_percentage = overrides.get("progress_percentage", 100)
        elif status == "in_progress":
            translated_content = overrides.get("translated_content", fake.text(max_nb_chars=2500))
            progress_percentage = overrides.get("progress_percentage", 50)
        else:  # pending or failed
            translated_content = overrides.get("translated_content")
            progress_percentage = overrides.get("progress_percentage", 0)

        # Build translation data
        translation_data = {
            "document_id": document_id,
            "target_language": overrides.get("target_language", "es"),
            "translated_content": translated_content,
            "status": status,
            "progress_percentage": progress_percentage,
            "translation_state": overrides.get("translation_state"),
            "user_id": overrides.get("user_id"),
            "session_id": overrides.get("session_id", str(uuid.uuid4())),
        }

        # Create translation instance
        translation = Translation(**translation_data)
        session.add(translation)
        return translation

    @staticmethod
    def create_translation_dict(
        document_id: uuid.UUID,
        overrides: Optional[dict] = None,
    ) -> dict:
        """
        Create a dictionary representing a translation (for API testing).

        Args:
            document_id: ID of the document being translated (required)
            overrides: Dictionary of field overrides

        Returns:
            Dictionary with translation data
        """
        if overrides is None:
            overrides = {}

        status = overrides.get("status", "pending")
        if status == "completed":
            translated_content = overrides.get("translated_content", fake.text(max_nb_chars=5000))
            progress_percentage = 100
        elif status == "in_progress":
            translated_content = overrides.get("translated_content", fake.text(max_nb_chars=2500))
            progress_percentage = 50
        else:
            translated_content = overrides.get("translated_content")
            progress_percentage = 0

        return {
            "document_id": str(document_id),
            "target_language": overrides.get("target_language", "es"),
            "translated_content": translated_content,
            "status": status,
            "progress_percentage": progress_percentage,
            "translation_state": overrides.get("translation_state"),
            "session_id": overrides.get("session_id", str(uuid.uuid4())),
        }

