"""
Document model.

Represents an uploaded TXT file that serves as the source for translation.
"""
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    DateTime,
    CheckConstraint,
    ForeignKey,
    Index,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.translation import Translation


class Document(Base):
    """Document model representing uploaded TXT files."""
    
    __tablename__ = "documents"
    
    # Primary key
    id: uuid.UUID = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=func.uuid_generate_v4(),
    )
    
    # Document content
    content: str = Column(Text, nullable=False)
    file_name: str = Column(String(255), nullable=False)
    file_size: int = Column(Integer, nullable=False)
    source_language: str = Column(String(10), nullable=False)  # ISO 639-1 code
    
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
    # user: Optional["User"] - defined via relationship()
    # translations: list["Translation"] - defined via relationship()
    user = relationship("User", back_populates="documents")
    translations = relationship(
        "Translation",
        back_populates="document",
        cascade="all, delete-orphan",
    )
    
    # Table constraints
    __table_args__ = (
        # File size check constraint (0 < file_size <= 10MB)
        CheckConstraint(
            "file_size > 0 AND file_size <= 10485760",
            name="documents_file_size_check",
        ),
        # User or session check constraint
        CheckConstraint(
            "(user_id IS NOT NULL) OR (session_id IS NOT NULL)",
            name="documents_user_or_session",
        ),
        # Indexes
        Index("idx_documents_user_id", "user_id", postgresql_where=text("user_id IS NOT NULL")),
        Index("idx_documents_session_id", "session_id", postgresql_where=text("session_id IS NOT NULL")),
        Index("idx_documents_created_at", text("created_at DESC")),
        # Full-text search index
        Index(
            "idx_documents_content_fts",
            text("to_tsvector('english', content)"),
            postgresql_using="gin",
        ),
    )
    
    def __repr__(self) -> str:
        return f"<Document(id={self.id}, file_name={self.file_name}, source_language={self.source_language})>"

