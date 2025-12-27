"""
Translation model.

Represents a translation of a document into a specific target language.
"""
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Dict, Any

from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    DateTime,
    CheckConstraint,
    ForeignKey,
    UniqueConstraint,
    Index,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.document import Document


class Translation(Base):
    """Translation model representing translated documents."""
    
    __tablename__ = "translations"
    
    # Primary key
    id: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4(),
    )
    
    # Translation attributes
    document_id: uuid.UUID = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    target_language: str = Column(String(10), nullable=False)  # ISO 639-1 code
    translated_content: Optional[str] = Column(Text, nullable=True)
    status: str = Column(
        String(20),
        nullable=False,
        server_default="pending",
    )  # 'pending', 'in_progress', 'completed', 'failed'
    progress_percentage: int = Column(
        Integer,
        nullable=False,
        server_default="0",
    )
    translation_state: Optional[Dict[str, Any]] = Column(JSONB, nullable=True)
    
    # User and session association
    user_id: Optional[uuid.UUID] = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    session_id: Optional[str] = Column(String(255), nullable=True)
    
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
    # document: "Document" - defined via relationship()
    # user: Optional["User"] - defined via relationship()
    document = relationship("Document", back_populates="translations")
    user = relationship("User", back_populates="translations")
    
    # Table constraints
    __table_args__ = (
        # Status enum check constraint
        CheckConstraint(
            "status IN ('pending', 'in_progress', 'completed', 'failed')",
            name="translations_status_check",
        ),
        # Progress percentage check constraint (0-100)
        CheckConstraint(
            "progress_percentage >= 0 AND progress_percentage <= 100",
            name="translations_progress_check",
        ),
        # User or session check constraint
        CheckConstraint(
            "(user_id IS NOT NULL) OR (session_id IS NOT NULL)",
            name="translations_user_or_session",
        ),
        # Unique constraint: one translation per document+target_language
        UniqueConstraint("document_id", "target_language", name="unique_document_target_language"),
        # Indexes
        Index("idx_translations_document_id", "document_id"),
        Index("idx_translations_user_id", "user_id", postgresql_where=text("user_id IS NOT NULL")),
        Index("idx_translations_session_id", "session_id", postgresql_where=text("session_id IS NOT NULL")),
        Index("idx_translations_status", "status"),
        Index("idx_translations_created_at", text("created_at DESC")),
        # Full-text search index
        Index(
            "idx_translations_content_fts",
            text("to_tsvector('english', translated_content)"),
            postgresql_where=text("translated_content IS NOT NULL"),
            postgresql_using="gin",
        ),
    )
    
    def __repr__(self) -> str:
        return f"<Translation(id={self.id}, document_id={self.document_id}, target_language={self.target_language}, status={self.status})>"

