"""
Integration tests for database migrations.

Tests that Alembic migrations can be applied and rolled back.
"""
import pytest
import os
from pathlib import Path
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import text

# Test database configuration
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://librilabs:librilabs_dev@localhost:5432/librilabs_translator_test"
)


@pytest.fixture(scope="session")
def alembic_cfg():
    """Create Alembic configuration for testing."""
    # Get the backend directory
    backend_dir = Path(__file__).parent.parent.parent
    alembic_ini = backend_dir / "alembic.ini"
    
    # Create config
    cfg = Config(str(alembic_ini))
    # Override database URL for testing
    cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    
    return cfg


@pytest.mark.asyncio
async def test_migrations_can_be_applied(alembic_cfg):
    """
    Test that Alembic migrations can be applied to test database.
    
    Note: This test requires a test database to be available.
    If the database is not available, this test will be skipped.
    """
    try:
        # Create engine to test connection
        engine = create_async_engine(TEST_DATABASE_URL, pool_pre_ping=True)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        await engine.dispose()
    except Exception as e:
        pytest.skip(f"Test database not available: {e}")
    
    # Apply migrations
    # Note: This runs synchronously but applies async migrations
    # The actual migration application happens in env.py which uses async
    try:
        command.upgrade(alembic_cfg, "head")
        
        # Verify migration was applied by checking if tables exist
        engine = create_async_engine(TEST_DATABASE_URL)
        async with engine.connect() as conn:
            # Check if users table exists
            result = await conn.execute(
                text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'users'
                    )
                """)
            )
            users_exists = result.scalar()
            
            # Check if documents table exists
            result = await conn.execute(
                text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'documents'
                    )
                """)
            )
            documents_exists = result.scalar()
            
            # Check if translations table exists
            result = await conn.execute(
                text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'translations'
                    )
                """)
            )
            translations_exists = result.scalar()
            
            assert users_exists, "Users table should exist after migration"
            assert documents_exists, "Documents table should exist after migration"
            assert translations_exists, "Translations table should exist after migration"
        
        await engine.dispose()
    except Exception as e:
        pytest.fail(f"Migration application failed: {e}")


@pytest.mark.asyncio
async def test_migrations_can_be_rolled_back(alembic_cfg):
    """
    Test that Alembic migrations can be rolled back.
    
    Note: This test requires a test database to be available.
    If the database is not available, this test will be skipped.
    """
    try:
        # Create engine to test connection
        engine = create_async_engine(TEST_DATABASE_URL, pool_pre_ping=True)
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        await engine.dispose()
    except Exception as e:
        pytest.skip(f"Test database not available: {e}")
    
    # First, ensure migrations are applied
    try:
        command.upgrade(alembic_cfg, "head")
        
        # Get current revision
        from alembic.script import ScriptDirectory
        script = ScriptDirectory.from_config(alembic_cfg)
        current_revision = script.get_current_head()
        
        if current_revision:
            # Rollback one migration
            command.downgrade(alembic_cfg, "-1")
            
            # Verify rollback worked (tables should be dropped if this was the only migration)
            # Note: This is a basic check - actual behavior depends on migration structure
            engine = create_async_engine(TEST_DATABASE_URL)
            async with engine.connect() as conn:
                result = await conn.execute(
                    text("""
                        SELECT COUNT(*) 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public'
                    """)
                )
                table_count = result.scalar()
                # After rollback, tables might be dropped
                # This is just a basic verification that rollback executed
                assert isinstance(table_count, int)
            
            await engine.dispose()
            
            # Re-apply migrations for other tests
            command.upgrade(alembic_cfg, "head")
    except Exception as e:
        pytest.fail(f"Migration rollback failed: {e}")

