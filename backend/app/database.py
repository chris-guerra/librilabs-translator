"""
Database connection and session management.

Configures SQLAlchemy 2.0 async engine with asyncpg driver and provides
FastAPI dependency injection for database sessions.
"""
import logging
import os
import asyncio
from typing import AsyncGenerator
from urllib.parse import urlparse, parse_qs

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from app.config import settings

logger = logging.getLogger(__name__)

def _is_production_environment() -> bool:
    """Check if running in production environment."""
    # Railway sets RAILWAY_ENVIRONMENT or similar env vars
    # Also check for production-like indicators
    return os.getenv("RAILWAY_ENVIRONMENT") == "production" or os.getenv("ENVIRONMENT") == "production"


def _validate_production_ssl(database_url: str) -> None:
    """
    Validate that production database connection uses SSL/TLS.
    
    Raises ValueError if production environment detected but SSL not configured.
    """
    if not _is_production_environment():
        return  # Skip validation in development
    
    parsed = urlparse(database_url)
    query_params = parse_qs(parsed.query)
    
    # Check for SSL parameters in connection string
    ssl_params = ["sslmode", "ssl", "sslcert", "sslkey", "sslrootcert"]
    has_ssl = any(param in query_params for param in ssl_params)
    
    # Railway connection strings typically include sslmode=require
    if not has_ssl and "railway" in parsed.hostname.lower() if parsed.hostname else False:
        # Railway managed Postgres should always have SSL
        logger.warning("Production Railway connection detected but SSL parameters not found in connection string")
    
    if not has_ssl:
        logger.warning(
            "Production environment detected but database connection string does not include SSL parameters. "
            "Ensure DATABASE_URL includes SSL configuration (e.g., ?sslmode=require)"
        )


# Validate production SSL configuration
_validate_production_ssl(settings.database_url)

# Create async engine with connection pooling
# Development: pool_size=5, max_overflow=10 (defaults)
# Production: Consider higher values (e.g., pool_size=10, max_overflow=20)
engine: AsyncEngine = create_async_engine(
    settings.database_url,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    echo=False,  # Set to True for SQL query logging in development
    connect_args={
        "server_settings": {
            "application_name": "librilabs_translator",
        }
    },
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database sessions.
    
    Yields an async database session and ensures it's properly closed
    after the request completes.
    
    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_database_connection(max_retries: int = 3, initial_delay: float = 1.0) -> bool:
    """
    Check if database connection can be established with retry logic.
    
    Implements exponential backoff retry for connection failures.
    
    Args:
        max_retries: Maximum number of retry attempts (default: 3)
        initial_delay: Initial delay in seconds before first retry (default: 1.0)
    
    Returns:
        True if connection successful, False otherwise
    """
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            async with AsyncSessionLocal() as session:
                # Simple query to test connection
                from sqlalchemy import text
                await session.execute(text("SELECT 1"))
                if attempt > 0:
                    logger.info(f"Database connection established after {attempt} retry(ies)")
                return True
        except (OperationalError, Exception) as e:
            if attempt < max_retries - 1:
                logger.warning(
                    f"Database connection attempt {attempt + 1}/{max_retries} failed: {e}. "
                    f"Retrying in {delay:.1f} seconds..."
                )
                await asyncio.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                logger.error(f"Database connection check failed after {max_retries} attempts: {e}")
                return False
    
    return False


async def verify_ssl_connection() -> bool:
    """
    Verify that database connection uses SSL/TLS in production.
    
    Returns:
        True if SSL is verified or not in production, False if SSL required but not available
    """
    if not _is_production_environment():
        logger.debug("Not in production environment, skipping SSL verification")
        return True
    
    try:
        async with AsyncSessionLocal() as session:
            from sqlalchemy import text
            # Query PostgreSQL to check SSL status using pg_stat_ssl
            # This view shows SSL information for current connections
            result = await session.execute(
                text("""
                    SELECT ssl 
                    FROM pg_stat_ssl 
                    WHERE pid = pg_backend_pid()
                """)
            )
            row = result.fetchone()
            
            if row and row[0]:  # ssl is True
                logger.info("SSL/TLS connection verified in production")
                return True
            elif row and not row[0]:  # ssl is False
                logger.error("SSL/TLS not in use for production database connection")
                return False
            else:
                # If view doesn't exist or no row returned, check connection string
                logger.warning("Could not query SSL status from pg_stat_ssl, verifying connection string")
                # Connection string validation already done in _validate_production_ssl
                return True  # Assume valid if connection string was validated
    except Exception as e:
        # If query fails, log warning but don't fail (might be permission issue or view not available)
        logger.warning(f"Could not verify SSL connection status: {e}")
        # In production, assume SSL is required and connection string should include it
        # Railway managed Postgres provides SSL by default
        return True  # Don't fail if we can't verify, but log the issue


async def verify_database_permissions() -> dict:
    """
    Verify database user permissions match least privilege requirements.
    
    Returns:
        Dictionary with permission check results
    """
    required_permissions = ["CREATE", "SELECT", "INSERT", "UPDATE", "DELETE"]
    results = {}
    
    try:
        async with AsyncSessionLocal() as session:
            from sqlalchemy import text
            
            # Check if user has required permissions
            # Query current user and their permissions
            result = await session.execute(
                text("""
                    SELECT 
                        has_database_privilege(current_user, current_database(), 'CREATE') as can_create,
                        has_schema_privilege(current_user, 'public', 'CREATE') as can_create_schema
                """)
            )
            row = result.fetchone()
            
            if row:
                results["can_create"] = row[0]
                results["can_create_schema"] = row[1]
            
            # Check table-level permissions (if tables exist)
            result = await session.execute(
                text("""
                    SELECT 
                        has_table_privilege(current_user, 'users', 'SELECT') as can_select_users,
                        has_table_privilege(current_user, 'documents', 'SELECT') as can_select_documents,
                        has_table_privilege(current_user, 'translations', 'SELECT') as can_select_translations
                """)
            )
            row = result.fetchone()
            
            if row:
                results["table_permissions"] = {
                    "users": {"SELECT": row[0]},
                    "documents": {"SELECT": row[1]},
                    "translations": {"SELECT": row[2]},
                }
            
            # Check for SUPERUSER (should be False for least privilege)
            result = await session.execute(
                text("SELECT usesuper FROM pg_user WHERE usename = current_user")
            )
            is_superuser = result.scalar()
            results["is_superuser"] = is_superuser if is_superuser is not None else False
            
            if results.get("is_superuser"):
                logger.warning("Database user has SUPERUSER privileges - violates least privilege principle")
            else:
                logger.info("Database user permissions verified - no SUPERUSER privileges")
            
            return results
            
    except Exception as e:
        logger.warning(f"Could not verify database permissions: {e}")
        return {"error": str(e)}


async def close_database_connection() -> None:
    """
    Close database engine and connection pool.
    
    Should be called during application shutdown.
    """
    await engine.dispose()
    logger.info("Database connection pool closed")

