"""
User factory for creating test users.

Uses faker to generate unique test data and supports overrides for explicit test intent.
Note: User model is for post-MVP authentication, but factory is included for future use.
"""
from typing import Optional
from faker import Faker

from app.models.user import User

fake = Faker()


class UserFactory:
    """Factory for creating User test data."""

    @staticmethod
    def create_user(
        session,
        overrides: Optional[dict] = None,
    ) -> User:
        """
        Create a User instance with sensible defaults.

        Args:
            session: Database session for persisting the user
            overrides: Dictionary of field overrides

        Returns:
            User instance (not yet committed to database)
        """
        if overrides is None:
            overrides = {}

        # Build user data
        user_data = {
            "email": overrides.get("email", fake.unique.email()),
        }

        # Create user instance
        user = User(**user_data)
        session.add(user)
        return user

    @staticmethod
    def create_user_dict(overrides: Optional[dict] = None) -> dict:
        """
        Create a dictionary representing a user (for API testing).

        Args:
            overrides: Dictionary of field overrides

        Returns:
            Dictionary with user data
        """
        if overrides is None:
            overrides = {}

        return {
            "email": overrides.get("email", fake.unique.email()),
        }

