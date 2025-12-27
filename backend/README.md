# Backend Setup Guide

## Security Validation

Before deploying, run the security validation script to ensure all security measures are in place:

```bash
./scripts/validate-security.sh
```

This script checks:
- `.env` is in `.gitignore`
- `.env.example` exists and doesn't contain actual keys
- No hardcoded API keys in source code
- Pre-commit hooks are configured
- CORS doesn't use wildcards
- Security documentation exists
- All security tests pass

## Local Development Setup

### Prerequisites

- Python 3.14 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Environment Setup

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your OpenAI API key (see OpenAI API Key Setup section below)

### Running the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/integration/test_routers/test_health.py
```

### Test Database Setup

Tests use a separate test database to avoid affecting development data. The test database is configured via the `TEST_DATABASE_URL` environment variable.

**Default Test Database:**
- URL: `postgresql+asyncpg://librilabs:librilabs_dev@localhost:5432/librilabs_translator_test`
- Database name: `librilabs_translator_test` (different from development database)

**Test Database Fixtures:**
- `test_engine`: Creates test database engine (session-scoped)
- `setup_test_database`: Sets up test database schema (creates/drops tables)
- `test_db_session`: Provides isolated database session for each test (auto-rollback)

**Running Tests with Test Database:**
1. Ensure PostgreSQL is running (Docker Compose or local instance)
2. Create test database (if it doesn't exist):
   ```bash
   # Using Docker Compose PostgreSQL
   docker-compose exec postgres psql -U librilabs -c "CREATE DATABASE librilabs_translator_test;"
   ```
3. Set `TEST_DATABASE_URL` in `.env` (optional, defaults to test database URL)
4. Run tests:
   ```bash
   pytest
   ```

**Test Database Behavior:**
- Tables are created before tests and dropped after tests (session scope)
- Each test gets a fresh transaction that is rolled back automatically
- Tests are isolated and don't affect each other
- Test database is separate from development database

## OpenAI API Key Setup

### Getting Your API Key

1. **Create an OpenAI Account:**
   - Visit https://platform.openai.com/
   - Sign up for an account or log in

2. **Generate API Key:**
   - Navigate to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Give it a name (e.g., "Librilabs Translator Dev")
   - Copy the key immediately (you won't be able to see it again)

3. **Configure in Project:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and set your API key:
     ```
     OPENAI_API_KEY=sk-your-actual-api-key-here
     ```

### Usage Limits and Rate Limits

- **Free Tier:** Limited requests per minute
- **Paid Tier:** Higher rate limits based on your plan
- **Rate Limits:** Check your usage dashboard at https://platform.openai.com/usage
- **Best Practice:** Implement retry logic with exponential backoff for production

### Security Best Practices

⚠️ **CRITICAL: Never commit API keys to version control**

1. **Environment Variables Only:**
   - Always use environment variables for API keys
   - Never hardcode keys in source code
   - Never log API key values (mask if referenced)

2. **Git Configuration:**
   - `.env` file is already in `.gitignore`
   - Verify `.env` is never committed:
     ```bash
     git check-ignore .env  # Should return: .env
     ```

3. **Pre-commit Hooks (REQUIRED):**
   Pre-commit hooks are configured to automatically detect and prevent secret commits.
   
   **Installation:**
   ```bash
   pip install pre-commit
   pre-commit install
   ```
   
   **Create secrets baseline (first time only):**
   ```bash
   pip install detect-secrets
   detect-secrets scan > .secrets.baseline
   git add .secrets.baseline
   ```
   
   **Verify hooks work:**
   ```bash
   pre-commit run --all-files
   ```
   
   The hooks will automatically:
   - Detect private keys, AWS credentials, and other secrets
   - Prevent commits containing secrets
   - Check for common security issues

4. **Production Deployment:**
   - Use secure secret management (Railway environment variables, AWS Secrets Manager, etc.)
   - Rotate keys regularly
   - Use different keys for development and production
   - See `SECURITY.md` for comprehensive security guidelines

### Troubleshooting

**Application fails to start if OPENAI_API_KEY is not set:**
- The application will log a warning but continue to run
- API key is only required when making OpenAI API calls (future stories)
- For now, you can run the application without the key for health check testing

## CORS Configuration

The application is configured with CORS middleware to allow requests from the frontend:

- **Development:** Allows `http://localhost:3000` (frontend dev server)
- **Production:** Must be configured with explicit allowed origins (never use `["*"]`)

**Production Configuration:**
- Set `ALLOWED_ORIGINS` environment variable with comma-separated origins
- Example: `ALLOWED_ORIGINS=https://app.librilabs.com,https://www.librilabs.com`
- Never use `allow_origins=["*"]` in production for security reasons
- Update `backend/app/main.py` to read from environment variable:
  ```python
  import os
  allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
  app.add_middleware(
      CORSMiddleware,
      allow_origins=allowed_origins,
      ...
  )
  ```

**Security:** See `SECURITY.md` for detailed CORS security guidelines

## Testing Infrastructure

This document describes the testing setup for the backend application.

### Testing Framework: Pytest

Pytest is the standard Python testing framework used for unit and integration testing.

#### Installation

```bash
pip install pytest pytest-asyncio
```

- `pytest`: Core testing framework
- `pytest-asyncio`: Required for testing async FastAPI endpoints

### API Testing: httpx

httpx is used as an async HTTP client for testing FastAPI endpoints.

#### Installation

```bash
pip install httpx
```

### Test Configuration

Create a `pytest.ini` file in the backend root directory:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
```

Alternatively, configure in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
```

### Test Structure

Backend tests should be organized as follows:

```
backend/tests/
├── unit/
│   ├── test_services/
│   └── test_models/
└── integration/
    └── test_routers/
```

### Example Test Structure

```python
# backend/tests/unit/test_services/example_test.py
import pytest
from app.services.example_service import ExampleService

def test_example_service_function():
    service = ExampleService()
    result = service.example_function()
    assert result is not None

# backend/tests/integration/test_routers/example_test.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_example_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/example")
        assert response.status_code == 200
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_services/example_test.py

# Run with coverage
pytest --cov=app --cov-report=html
```

### Note

Backend testing implementation will be completed in Story 1.1. This document serves as a reference for the testing infrastructure setup.

## Database Migrations with Alembic

Alembic is used for database schema versioning and migrations. The database uses PostgreSQL with SQLAlchemy 2.0 async support.

### Prerequisites

- PostgreSQL database running (via Docker Compose or Railway)
- `DATABASE_URL` environment variable configured (see `.env.example`)

### Common Alembic Commands

#### Apply Migrations

Apply all pending migrations to bring the database up to date:

```bash
alembic upgrade head
```

#### Create a New Migration

Create a new migration file (auto-generate from model changes):

```bash
alembic revision --autogenerate -m "description_of_changes"
```

Create an empty migration file (manual migration):

```bash
alembic revision -m "description_of_changes"
```

#### Rollback Migrations

Rollback one migration:

```bash
alembic downgrade -1
```

Rollback to a specific revision:

```bash
alembic downgrade <revision_id>
```

#### Check Current Migration Status

View current database revision:

```bash
alembic current
```

View migration history:

```bash
alembic history
```

### Migration Naming Convention

Migrations follow the pattern: `{revision_id}_{description}.py`

Example: `813dd91d1bac_initial_schema.py`

### Connection Pool Sizing

**Development:**
- Default pool settings: `pool_size=5`, `max_overflow=10`
- Sufficient for local development and testing

**Production:**
- Consider higher values based on expected load
- Recommended: `pool_size=10`, `max_overflow=20` (or higher)
- Monitor connection pool usage to optimize settings
- Balance resource usage with performance needs

### Database Setup

1. **Local Development (Docker Compose):**
   - PostgreSQL runs in Docker container
   - Connection string: `postgresql+asyncpg://librilabs:librilabs_dev@postgres:5432/librilabs_translator`
   - Set `DATABASE_URL` in `.env` file

2. **Production (Railway):**
   - Railway managed Postgres provides connection string
   - Set `DATABASE_URL` via Railway environment variables
   - SSL/TLS is enabled by default

### Database Configuration

#### Local Development Setup (Docker Compose)

For local development, PostgreSQL runs in a Docker container via Docker Compose.

1. **Start PostgreSQL:**
   ```bash
   docker-compose up -d postgres
   ```

2. **Configure DATABASE_URL in `.env`:**
   ```bash
   # Copy .env.example to .env if it doesn't exist
   cp .env.example .env
   
   # Edit .env and set DATABASE_URL:
   DATABASE_URL=postgresql+asyncpg://librilabs:librilabs_dev@postgres:5432/librilabs_translator
   ```

3. **Verify connection:**
   ```bash
   # Check if PostgreSQL is running
   docker-compose ps postgres
   
   # Test connection (from backend container or local Python)
   python -c "from app.database import check_database_connection; import asyncio; print(asyncio.run(check_database_connection()))"
   ```

**Docker Compose Configuration:**
- PostgreSQL service: `postgres:16`
- Default credentials: `librilabs` / `librilabs_dev`
- Database name: `librilabs_translator`
- Port: `5432` (mapped to host)
- Health check: Configured to wait for PostgreSQL to be ready
- Backend service depends on PostgreSQL health check

#### Production Setup (Railway)

For production, use Railway managed PostgreSQL.

1. **Create PostgreSQL service in Railway:**
   - Add PostgreSQL service to your Railway project
   - Railway provides connection string automatically

2. **Set DATABASE_URL environment variable:**
   - In Railway dashboard, add `DATABASE_URL` environment variable
   - Use the connection string provided by Railway
   - Format: `postgresql+asyncpg://user:password@host:port/dbname`
   - Railway includes SSL parameters in the connection string

3. **Verify SSL/TLS:**
   - Railway managed Postgres provides SSL/TLS by default
   - Connection string includes SSL parameters
   - SSL verification is automatically performed in production
   - Use `verify_ssl_connection()` function to explicitly verify SSL status
   - Check production logs for SSL verification messages

### Security Considerations

#### SQL Injection Protection

**SQLAlchemy ORM Protection:**
- SQLAlchemy ORM automatically parameterizes all queries
- Provides built-in protection against SQL injection attacks
- Never use raw SQL queries with string formatting
- Always use SQLAlchemy ORM methods and query builders

**Best Practices:**
```python
# ✅ GOOD: Use ORM methods
result = await session.execute(select(Document).where(Document.id == document_id))

# ❌ BAD: Never use string formatting with raw SQL
# result = await session.execute(f"SELECT * FROM documents WHERE id = '{document_id}'")
```

#### SSL/TLS Requirements

**Production:**
- Production database connections **must** use SSL/TLS encryption
- Railway managed Postgres provides SSL/TLS by default
- Connection string includes SSL parameters automatically
- Verify SSL connection in production environment

**Local Development:**
- Docker Compose PostgreSQL does not require SSL (local network)
- Production connections must be encrypted
- Never use unencrypted connections in production

#### Database User Permissions

**Least Privilege Principle:**
- Database user should only have necessary permissions
- Required permissions: `CREATE` (for migrations), `SELECT`, `INSERT`, `UPDATE`, `DELETE` on application tables
- Do not grant `SUPERUSER` or unnecessary administrative privileges
- Railway managed Postgres creates users with appropriate permissions by default

#### Connection String Security

**Never Commit Credentials:**
- ❌ Never commit database credentials to version control
- ✅ Always use environment variables for database connection strings
- ✅ Use `.env.example` as a template (without actual credentials)
- ✅ Verify `.env` files are in `.gitignore`
- ✅ In production, use secure secret management (Railway environment variables)

**Environment Variable Management:**
```bash
# ✅ GOOD: Use .env file (not committed to git)
DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname

# ❌ BAD: Hardcoded in source code
# database_url = "postgresql+asyncpg://user:password@host:port/dbname"
```

**Error Handling:**
- Database connection errors should not expose sensitive information
- Log connection errors with appropriate detail level (no credentials in logs)
- Implement graceful degradation for database connection failures
- Connection retry logic with exponential backoff is implemented in `check_database_connection()`
- Retry attempts: 3 (configurable), initial delay: 1 second, exponential backoff

**SSL/TLS Verification:**
- Production environment automatically validates SSL/TLS connection
- `verify_ssl_connection()` function checks SSL status using PostgreSQL system views
- Connection string validation ensures SSL parameters are present in production
- Railway managed Postgres connections are automatically validated

**Database Permissions Verification:**
- `verify_database_permissions()` function checks user permissions
- Verifies least privilege principle (no SUPERUSER privileges)
- Checks required permissions: CREATE, SELECT, INSERT, UPDATE, DELETE
- Logs warnings if permissions exceed least privilege requirements

### Troubleshooting

**Migration fails with connection error:**
- Verify `DATABASE_URL` is set correctly in `.env` file
- Ensure PostgreSQL is running (Docker Compose: `docker-compose up postgres`)
- Check database credentials match Docker Compose configuration
- Verify network connectivity between backend and PostgreSQL containers

**Configuration validation fails:**
- Ensure `DATABASE_URL` is set in `.env` file (required, no default)
- Check `.env` file format matches `.env.example`
- Verify environment variables are loaded (check `app.config.settings.database_url`)

**Database connection timeout:**
- Verify PostgreSQL health check is passing: `docker-compose ps postgres`
- Check PostgreSQL logs: `docker-compose logs postgres`
- Verify backend service depends on PostgreSQL: `docker-compose config | grep depends_on`

**Autogenerate doesn't detect model changes:**
- Ensure models are imported in `alembic/env.py`
- Verify `target_metadata = Base.metadata` is set correctly
- Check that models inherit from `Base`

