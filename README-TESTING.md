# Testing Guide

This document explains how to run tests for both backend and frontend projects, either independently or together.

## Quick Start

### Run All Tests (Full Stack)
```bash
make test
```

### Run Backend Tests Only
```bash
make test-backend
# or
cd backend && make test
```

### Run Frontend Tests Only
```bash
make test-frontend
# or
cd frontend && make test
```

### Run Frontend E2E Tests
```bash
make test-e2e
# or
cd frontend && make test-e2e
```

## Backend Testing

### Prerequisites

The backend tests require:
- Docker and Docker Compose
- PostgreSQL (managed via Docker Compose)

### Running Tests

```bash
cd backend

# Run all tests
make test

# Run tests with coverage
make test-coverage

# Run specific test file
make test-file FILE=tests/integration/test_routers/test_health.py

# Run tests in verbose mode
make test-verbose
```

### Test Database

The backend uses a separate test database (`librilabs_translator_test`) that is automatically created and managed via Docker Compose. The test database runs on port `5433` (default PostgreSQL is on `5432`).

### Test Framework

- **Framework**: Pytest with pytest-asyncio
- **Test Client**: httpx AsyncClient
- **Data Factories**: Faker-based factories in `tests/support/factories/`
- **Fixtures**: Database fixtures with auto-rollback in `tests/conftest.py`

### Example Test

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
```

## Frontend Testing

### Prerequisites

The frontend tests require:
- Docker and Docker Compose
- Node.js 20+ (managed via Docker)
- Playwright browsers (installed automatically)

### Running Tests

```bash
cd frontend

# Run unit tests
make test

# Run unit tests in watch mode
make test-watch

# Run E2E tests
make test-e2e

# Run E2E tests in UI mode
make test-e2e-ui

# Run E2E tests in headed mode
make test-e2e-headed

# Install Playwright browsers (if needed)
make test-install-browsers
```

### Test Framework

- **Unit Tests**: Vitest + React Testing Library
- **E2E Tests**: Playwright
- **Data Factories**: Faker-based factories in `tests/support/factories/`
- **Fixtures**: Composable fixtures using `mergeTests` pattern

### Example Test

```typescript
import { test, expect } from '../support/fixtures';
import { createDocument } from '../support/factories';

test('should upload document', async ({ page, apiRequest }) => {
  const doc = createDocument({ content: 'Test content' });
  const uploaded = await apiRequest.createDocument(doc.content, doc.file_name);
  expect(uploaded.id).toBeTruthy();
});
```

## Docker Setup

### Backend Docker Setup

The backend Docker setup includes:
- **Main Database**: PostgreSQL on port 5432
- **Test Database**: PostgreSQL on port 5433 (profile: test)
- **Backend Service**: FastAPI on port 8000

### Frontend Docker Setup

The frontend Docker setup includes:
- **Frontend Service**: Next.js on port 3000
- **Playwright Browsers**: Installed in development image

### Full Stack Docker Setup

The root `docker-compose.yml` orchestrates all services:
- PostgreSQL (shared)
- Backend (FastAPI)
- Frontend (Next.js)

## Independent Project Testing

Both projects can run tests independently:

### Backend (Standalone)
```bash
cd backend
make test
```

### Frontend (Standalone)
```bash
cd frontend
make test
make test-e2e
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run backend tests
        run: |
          cd backend
          make test

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run frontend tests
        run: |
          cd frontend
          make test
          make test-e2e
```

## Troubleshooting

### Backend Tests Fail with Database Connection Error

1. Ensure test database is running:
   ```bash
   cd backend
   make test-db-setup
   ```

2. Check environment variables:
   ```bash
   # In backend/.env
   TEST_DATABASE_URL=postgresql+asyncpg://librilabs:librilabs_dev@localhost:5433/librilabs_translator_test
   ```

### Frontend E2E Tests Fail

1. Install Playwright browsers:
   ```bash
   cd frontend
   make test-install-browsers
   ```

2. Ensure backend is running (for E2E tests):
   ```bash
   # From root
   make up
   ```

### Tests Run Slowly

- Use parallel execution (default in Playwright)
- Use API setup instead of UI navigation
- Ensure Docker volumes are properly mounted

## Best Practices

1. **Use Factories**: Always use data factories for test data
2. **API-First Setup**: Use API helpers for fast data setup
3. **Parallel Safety**: All factories use faker for unique data
4. **Auto-Cleanup**: Database fixtures auto-rollback after tests
5. **Explicit Assertions**: Keep assertions visible in test bodies

## Documentation

- Backend test framework: `backend/tests/README.md`
- Frontend test framework: `frontend/tests/README.md`
- System-level test design: `_bmad-output/test-design-system.md`

