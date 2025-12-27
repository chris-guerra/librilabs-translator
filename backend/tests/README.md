# Backend Test Framework

This directory contains the test framework for the Librilabs Translator backend (FastAPI).

## Directory Structure

```
backend/tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── support/                 # Test infrastructure
│   ├── factories/          # Data factories (faker-based)
│   │   ├── document_factory.py
│   │   ├── translation_factory.py
│   │   └── user_factory.py
│   └── helpers/           # Pure helper functions
│       └── api_helpers.py
├── unit/                   # Unit tests
│   └── test_config.py
└── integration/            # Integration tests
    ├── test_database_connection.py
    ├── test_migrations.py
    ├── test_models.py
    └── test_routers/
        ├── test_health.py
        ├── test_cors.py
        └── test_error_handling.py
```

## Setup

### Prerequisites

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up test database:
```bash
# Ensure PostgreSQL is running (via Docker Compose)
export TEST_DATABASE_URL="postgresql+asyncpg://librilabs:librilabs_dev@localhost:5432/librilabs_translator_test"
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/integration/test_routers/test_health.py

# Run with coverage
pytest --cov=app --cov-report=html

# Run in verbose mode
pytest -v

# Run specific test
pytest tests/integration/test_routers/test_health.py::test_health_endpoint
```

## Test Architecture

### Fixtures

The test framework uses pytest fixtures for test setup and teardown:

- **`client`**: FastAPI test client (httpx AsyncClient)
- **`test_db_session`**: Isolated database session with auto-rollback
- **`document_factory`**: Factory for creating test documents
- **`translation_factory`**: Factory for creating test translations
- **`sample_document`**: Pre-created document fixture
- **`sample_translation`**: Pre-created translation fixture
- **`unique_session_id`**: Unique session ID for each test

### Data Factories

Factories use `faker` to generate unique test data and support overrides:

```python
from tests.support.factories import DocumentFactory

# Create document with defaults
document = DocumentFactory.create_document(session)

# Create document with overrides
document = DocumentFactory.create_document(
    session,
    overrides={
        "content": "Custom content",
        "source_language": "fr",
        "content_size": "large",  # small, medium, large
    }
)
```

### API Helpers

Pure functions for making API requests:

```python
from tests.support.helpers.api_helpers import create_document_via_api

# Create document via API
document = await create_document_via_api(
    client,
    file_content="Test content",
    file_name="test.txt",
    source_language="en",
    session_id="test-session-id",
)
```

## Best Practices

1. **Use Factories**: Always use factories for test data creation (not hardcoded values)
2. **Parallel Safety**: All factories use faker for unique data (no collisions in parallel runs)
3. **Auto-Cleanup**: Database fixtures auto-rollback after each test
4. **Explicit Assertions**: Keep assertions visible in test bodies
5. **API-First Setup**: Use API helpers for data setup (faster than UI)

## Test Organization

- **Unit Tests**: Test individual functions/classes in isolation
- **Integration Tests**: Test API endpoints, database operations, service layer
- **E2E Tests**: Test complete workflows (handled by frontend Playwright tests)

## Configuration

Test configuration is in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
```

## CI Integration

Tests run automatically in CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    cd backend
    pytest --cov=app --cov-report=xml
```

## Knowledge Base References

- `fixture-architecture.md` - Pure function → fixture pattern
- `data-factories.md` - Factory patterns with faker
- `test-quality.md` - Test design principles

