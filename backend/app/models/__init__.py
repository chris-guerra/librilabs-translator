"""
Database models.

This module exports all database models and the Base declarative base.
"""
from sqlalchemy.orm import declarative_base

# Create declarative base for all models
Base = declarative_base()

# Import all models to register them with Base
from app.models.user import User
from app.models.document import Document
from app.models.translation import Translation

# Set up relationships (import order matters for relationships)
# Relationships are defined in the model files themselves

__all__ = ["Base", "User", "Document", "Translation"]

