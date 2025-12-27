"""
Integration tests for database models.

Tests that models can be created, queried, and relationships work correctly.
"""
import pytest
import uuid
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import User, Document, Translation


@pytest.mark.asyncio
async def test_user_model_creation(test_db_session):
    """Test that User model can be created and queried."""
    # Create a user
    user = User(
        email="test@example.com",
    )
    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)
    
    # Verify user was created
    assert user.id is not None
    assert isinstance(user.id, uuid.UUID)
    assert user.email == "test@example.com"
    assert user.created_at is not None
    assert user.updated_at is not None
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.updated_at, datetime)


@pytest.mark.asyncio
async def test_document_model_creation(test_db_session):
    """Test that Document model can be created and queried."""
    # Create a document with session_id (MVP anonymous session)
    document = Document(
        content="Test document content",
        file_name="test.txt",
        file_size=100,
        source_language="en",
        session_id="test-session-123",
    )
    test_db_session.add(document)
    await test_db_session.commit()
    await test_db_session.refresh(document)
    
    # Verify document was created
    assert document.id is not None
    assert isinstance(document.id, uuid.UUID)
    assert document.content == "Test document content"
    assert document.file_name == "test.txt"
    assert document.file_size == 100
    assert document.source_language == "en"
    assert document.session_id == "test-session-123"
    assert document.user_id is None  # MVP uses session_id
    assert document.created_at is not None
    assert document.updated_at is not None


@pytest.mark.asyncio
async def test_translation_model_creation(test_db_session):
    """Test that Translation model can be created and queried."""
    # Create a document first
    document = Document(
        content="Test content",
        file_name="test.txt",
        file_size=50,
        source_language="en",
        session_id="test-session-123",
    )
    test_db_session.add(document)
    await test_db_session.commit()
    await test_db_session.refresh(document)
    
    # Create a translation
    translation = Translation(
        document_id=document.id,
        target_language="es",
        translated_content="Contenido de prueba",
        status="completed",
        progress_percentage=100,
        session_id="test-session-123",
    )
    test_db_session.add(translation)
    await test_db_session.commit()
    await test_db_session.refresh(translation)
    
    # Verify translation was created
    assert translation.id is not None
    assert isinstance(translation.id, uuid.UUID)
    assert translation.document_id == document.id
    assert translation.target_language == "es"
    assert translation.translated_content == "Contenido de prueba"
    assert translation.status == "completed"
    assert translation.progress_percentage == 100
    assert translation.session_id == "test-session-123"


@pytest.mark.asyncio
async def test_document_translation_relationship(test_db_session):
    """Test that Document-Translation relationship works."""
    # Create a document
    document = Document(
        content="Test content",
        file_name="test.txt",
        file_size=50,
        source_language="en",
        session_id="test-session-123",
    )
    test_db_session.add(document)
    await test_db_session.commit()
    await test_db_session.refresh(document)
    
    # Create translations
    translation1 = Translation(
        document_id=document.id,
        target_language="es",
        translated_content="Contenido",
        status="completed",
        progress_percentage=100,
        session_id="test-session-123",
    )
    translation2 = Translation(
        document_id=document.id,
        target_language="fr",
        translated_content="Contenu",
        status="completed",
        progress_percentage=100,
        session_id="test-session-123",
    )
    test_db_session.add_all([translation1, translation2])
    await test_db_session.commit()
    
    # Reload document with translations eagerly loaded (required for async SQLAlchemy)
    result = await test_db_session.execute(
        select(Document)
        .where(Document.id == document.id)
        .options(selectinload(Document.translations))
    )
    document_with_translations = result.scalar_one()
    
    # Verify relationship
    assert len(document_with_translations.translations) == 2
    translation_ids = [t.id for t in document_with_translations.translations]
    assert translation1.id in translation_ids
    assert translation2.id in translation_ids
    
    # Verify reverse relationship
    await test_db_session.refresh(translation1)
    await test_db_session.refresh(translation2)
    assert translation1.document_id == document.id
    assert translation2.document_id == document.id


@pytest.mark.asyncio
async def test_document_file_size_constraint(test_db_session):
    """Test that file_size check constraint works."""
    # Try to create document with invalid file_size (too large)
    document = Document(
        content="Test",
        file_name="test.txt",
        file_size=10485761,  # > 10MB
        source_language="en",
        session_id="test-session-123",
    )
    test_db_session.add(document)
    
    # Should raise constraint violation
    with pytest.raises(Exception):  # SQLAlchemy will raise an exception
        await test_db_session.commit()


@pytest.mark.asyncio
async def test_translation_status_constraint(test_db_session):
    """Test that status check constraint works."""
    document = Document(
        content="Test",
        file_name="test.txt",
        file_size=100,
        source_language="en",
        session_id="test-session-123",
    )
    test_db_session.add(document)
    await test_db_session.commit()
    await test_db_session.refresh(document)
    
    # Try to create translation with invalid status
    translation = Translation(
        document_id=document.id,
        target_language="es",
        status="invalid_status",  # Not in allowed enum
        progress_percentage=0,
        session_id="test-session-123",
    )
    test_db_session.add(translation)
    
    # Should raise constraint violation
    with pytest.raises(Exception):
        await test_db_session.commit()


@pytest.mark.asyncio
async def test_translation_progress_constraint(test_db_session):
    """Test that progress_percentage check constraint works."""
    document = Document(
        content="Test",
        file_name="test.txt",
        file_size=100,
        source_language="en",
        session_id="test-session-123",
    )
    test_db_session.add(document)
    await test_db_session.commit()
    await test_db_session.refresh(document)
    
    # Try to create translation with invalid progress (out of range)
    translation = Translation(
        document_id=document.id,
        target_language="es",
        status="pending",
        progress_percentage=101,  # > 100
        session_id="test-session-123",
    )
    test_db_session.add(translation)
    
    # Should raise constraint violation
    with pytest.raises(Exception):
        await test_db_session.commit()

