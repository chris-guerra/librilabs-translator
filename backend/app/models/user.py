"""
User model.

Represents authenticated users. Created for post-MVP authentication but not used in MVP.
"""
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models import Base

if TYPE_CHECKING:
    from app.models.document import Document
    from app.models.translation import Translation


class User(Base):
    """User model for post-MVP authentication."""
    
    __tablename__ = "users"
    
    # Primary key
    id: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4(),
    )
    
    # User attributes
    email: str = Column(String(255), unique=True, nullable=False)
    
    # Timestamps
    created_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
        onupdate=func.current_timestamp(),
    )
    
    # Relationships
    # documents: Mapped[List["Document"]] - defined via relationship()
    # translations: Mapped[List["Translation"]] - defined via relationship()
    documents = relationship(
        "Document",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    translations = relationship(
        "Translation",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"

