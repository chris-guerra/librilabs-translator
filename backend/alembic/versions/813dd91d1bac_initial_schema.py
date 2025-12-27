"""initial_schema

Revision ID: 813dd91d1bac
Revises: 
Create Date: 2025-11-29 14:20:19.361346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '813dd91d1bac'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema - create initial database structure."""
    # Enable UUID extension
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )
    
    # Create documents table
    op.create_table(
        'documents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('source_language', sa.String(10), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('session_id', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint('file_size > 0 AND file_size <= 10485760', name='documents_file_size_check'),
        sa.CheckConstraint('(user_id IS NOT NULL) OR (session_id IS NOT NULL)', name='documents_user_or_session'),
    )
    
    # Create translations table
    op.create_table(
        'translations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('document_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('target_language', sa.String(10), nullable=False),
        sa.Column('translated_content', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('progress_percentage', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('translation_state', postgresql.JSONB(), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('session_id', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint("status IN ('pending', 'in_progress', 'completed', 'failed')", name='translations_status_check'),
        sa.CheckConstraint('progress_percentage >= 0 AND progress_percentage <= 100', name='translations_progress_check'),
        sa.CheckConstraint('(user_id IS NOT NULL) OR (session_id IS NOT NULL)', name='translations_user_or_session'),
        sa.UniqueConstraint('document_id', 'target_language', name='unique_document_target_language'),
    )
    
    # Create indexes for documents table
    op.create_index('idx_documents_user_id', 'documents', ['user_id'], postgresql_where=sa.text('user_id IS NOT NULL'))
    op.create_index('idx_documents_session_id', 'documents', ['session_id'], postgresql_where=sa.text('session_id IS NOT NULL'))
    op.create_index('idx_documents_created_at', 'documents', [sa.text('created_at DESC')])
    op.create_index('idx_documents_content_fts', 'documents', [sa.text("to_tsvector('english', content)")], postgresql_using='gin')
    
    # Create indexes for translations table
    op.create_index('idx_translations_document_id', 'translations', ['document_id'])
    op.create_index('idx_translations_user_id', 'translations', ['user_id'], postgresql_where=sa.text('user_id IS NOT NULL'))
    op.create_index('idx_translations_session_id', 'translations', ['session_id'], postgresql_where=sa.text('session_id IS NOT NULL'))
    op.create_index('idx_translations_status', 'translations', ['status'])
    op.create_index('idx_translations_created_at', 'translations', [sa.text('created_at DESC')])
    op.create_index('idx_translations_content_fts', 'translations', [sa.text("to_tsvector('english', translated_content)")], postgresql_where=sa.text('translated_content IS NOT NULL'), postgresql_using='gin')
    
    # Create trigger function for updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)
    
    # Create triggers for updated_at on all tables
    op.execute("""
        CREATE TRIGGER update_documents_updated_at 
        BEFORE UPDATE ON documents
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)
    
    op.execute("""
        CREATE TRIGGER update_translations_updated_at 
        BEFORE UPDATE ON translations
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)
    
    op.execute("""
        CREATE TRIGGER update_users_updated_at 
        BEFORE UPDATE ON users
        FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
    """)


def downgrade() -> None:
    """Downgrade schema - remove all database structures."""
    # Drop triggers
    op.execute('DROP TRIGGER IF EXISTS update_users_updated_at ON users')
    op.execute('DROP TRIGGER IF EXISTS update_translations_updated_at ON translations')
    op.execute('DROP TRIGGER IF EXISTS update_documents_updated_at ON documents')
    
    # Drop trigger function
    op.execute('DROP FUNCTION IF EXISTS update_updated_at_column()')
    
    # Drop indexes
    op.drop_index('idx_translations_content_fts', table_name='translations')
    op.drop_index('idx_translations_created_at', table_name='translations')
    op.drop_index('idx_translations_status', table_name='translations')
    op.drop_index('idx_translations_session_id', table_name='translations')
    op.drop_index('idx_translations_user_id', table_name='translations')
    op.drop_index('idx_translations_document_id', table_name='translations')
    op.drop_index('idx_documents_content_fts', table_name='documents')
    op.drop_index('idx_documents_created_at', table_name='documents')
    op.drop_index('idx_documents_session_id', table_name='documents')
    op.drop_index('idx_documents_user_id', table_name='documents')
    
    # Drop tables (order matters due to foreign keys)
    op.drop_table('translations')
    op.drop_table('documents')
    op.drop_table('users')
    
    # Drop UUID extension
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
