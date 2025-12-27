"""
Data factories for creating test data.

Factories use faker to generate unique test data and support overrides
for explicit test intent. All factories are designed to be parallel-safe.
"""

from .document_factory import DocumentFactory
from .translation_factory import TranslationFactory
from .user_factory import UserFactory

__all__ = ["DocumentFactory", "TranslationFactory", "UserFactory"]

