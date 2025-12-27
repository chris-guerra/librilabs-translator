"""
Pytest configuration and fixtures.

Provides FastAPI test client fixture and database test fixtures for integration tests.
"""
import os
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker
from sqlalchemy import text

from app.main import app
from app.database import AsyncSessionLocal
from app.models import Base


@pytest.fixture(scope="session")
def event_loop():
    """
    Create a session-scoped event loop.
    
    This ensures all async fixtures and tests use the same event loop,
    preventing "attached to a different loop" errors.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    """
    FastAPI test client fixture.
    
    Provides an async HTTP client for testing FastAPI endpoints.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# Test database configuration
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://librilabs:librilabs_dev@localhost:5432/librilabs_translator_test"
)


# Global state for database setup (runs once per session)
_database_initialized = False


@pytest_asyncio.fixture(scope="session")
async def setup_test_database():
    """
    Set up test database schema once per session.
    
    This runs before any tests and sets up the database schema.
    """
    global _database_initialized
    
    if not _database_initialized:
        # Create a temporary engine just for setup
        setup_engine = create_async_engine(
            TEST_DATABASE_URL,
            pool_pre_ping=True,
            echo=False,
        )
        
        async with setup_engine.begin() as conn:
            # Enable UUID extension (required for uuid_generate_v4())
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
            # Drop all tables if they exist (for clean test runs)
            await conn.run_sync(Base.metadata.drop_all)
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        
        await setup_engine.dispose()
        _database_initialized = True
    
    yield
    
    # Cleanup after all tests
    cleanup_engine = create_async_engine(
        TEST_DATABASE_URL,
        pool_pre_ping=True,
        echo=False,
    )
    async with cleanup_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await cleanup_engine.dispose()


@pytest_asyncio.fixture
async def test_engine(setup_test_database):
    """
    Create test database engine for each test.
    
    Function-scoped to avoid event loop conflicts with asyncpg.
    """
    engine = create_async_engine(
        TEST_DATABASE_URL,
        pool_pre_ping=True,
        echo=False,
        pool_size=5,
        max_overflow=10,
    )
    
    yield engine
    
    # Dispose of the engine after each test
    await engine.dispose()


@pytest_asyncio.fixture
async def test_db_session(test_engine: AsyncEngine):
    """
    Create a test database session.
    
    Provides a database session for each test, with automatic rollback.
    """
    # Create session factory
    TestSessionLocal = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    
    # Create a new session for each test
    session = TestSessionLocal()
    try:
        # Start a transaction
        await session.begin()
        yield session
    finally:
        # Rollback transaction to keep test database clean
        await session.rollback()
        await session.close()


@pytest.fixture
async def db_session():
    """
    Database session fixture using the application's database.
    
    This fixture uses the actual database connection from app.database.
    Use test_db_session for isolated test database operations.
    """
    async for session in AsyncSessionLocal():
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

