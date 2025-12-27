# Docker Setup Guide

This guide explains how to use Docker for development and testing of both backend and frontend projects independently or together.

## Architecture

Both backend and frontend are **independent projects** that can be:
- Run separately with their own Docker Compose files
- Orchestrated together via root `docker-compose.yml`
- Separated into different repositories if needed

## Quick Start

### Run Everything Together
```bash
# From project root
make up-dev
```

### Run Backend Only
```bash
cd backend
make up-dev
```

### Run Frontend Only
```bash
cd frontend
make up-dev
```

## Backend Docker Setup

### Structure
- **Dockerfile**: Multi-stage build (builder + runtime)
- **docker-compose.yml**: Backend + PostgreSQL
- **Makefile**: Development commands

### Services
- **backend**: FastAPI application (port 8000)
- **postgres**: PostgreSQL database (port 5432)
- **postgres-test**: Test database (port 5433, profile: test)

### Commands
```bash
cd backend

# Build and start
make build
make up-dev

# Run tests
make test
make test-coverage

# View logs
make logs
make logs-backend

# Stop
make down
```

### Environment Variables
Create `backend/.env`:
```bash
DATABASE_URL=postgresql+asyncpg://librilabs:librilabs_dev@postgres:5432/librilabs_translator
TEST_DATABASE_URL=postgresql+asyncpg://librilabs:librilabs_dev@postgres-test:5432/librilabs_translator_test
OPENAI_API_KEY=your_key_here
```

## Frontend Docker Setup

### Structure
- **Dockerfile**: Multi-stage build (deps + builder + runtime + development)
- **docker-compose.yml**: Frontend service
- **Makefile**: Development commands

### Services
- **frontend**: Next.js application (port 3000)

### Commands
```bash
cd frontend

# Build and start
make build
make up-dev

# Run tests
make test
make test-e2e

# View logs
make logs

# Stop
make down
```

### Environment Variables
Create `frontend/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:8000
```

## Full Stack Docker Setup

### Root docker-compose.yml
Orchestrates all services:
- PostgreSQL (shared)
- Backend (FastAPI)
- Frontend (Next.js)
- Test database (profile: test)

### Commands
```bash
# From project root

# Start all services
make up-dev

# Run all tests
make test

# Run backend tests
make test-backend

# Run frontend tests
make test-frontend

# Run frontend E2E tests
make test-e2e

# View logs
make logs
make logs-backend
make logs-frontend

# Stop all
make down
```

## Testing in Docker

### Backend Tests
```bash
cd backend

# Run all tests (auto-starts test database)
make test

# Run with coverage
make test-coverage

# Run specific file
make test-file FILE=tests/integration/test_routers/test_health.py
```

**Test Database:**
- Automatically created via Docker Compose profile
- Runs on port 5433 (separate from main DB on 5432)
- Auto-starts before tests, auto-stops after

### Frontend Tests
```bash
cd frontend

# Run unit tests
make test

# Run E2E tests
make test-e2e

# Run E2E in UI mode
make test-e2e-ui

# Install Playwright browsers (first time)
make test-install-browsers
```

**Playwright Setup:**
- Browsers installed in Docker image
- Test results mounted to host: `./test-results/`
- Reports mounted to host: `./playwright-report/`

## Dependencies

### Backend Dependencies
All dependencies (including test dependencies) are installed in Docker:
- Production: `requirements.txt`
- Test: `faker`, `pytest`, `pytest-asyncio`, `httpx`

### Frontend Dependencies
All dependencies (including test dependencies) are installed in Docker:
- Production: `package.json` dependencies
- Test: `@faker-js/faker`, `@playwright/test`, `vitest`, `@testing-library/react`

## Volume Mounts

### Backend
- Source code: `./backend:/app` (hot-reload)
- Virtual environment: `/app/.venv` (excluded from mount)

### Frontend
- Source code: `./frontend:/app` (hot-reload)
- node_modules: `/app/node_modules` (excluded from mount)
- .next: `/app/.next` (excluded from mount)
- Test results: `./frontend/test-results:/app/test-results`
- Reports: `./frontend/playwright-report:/app/playwright-report`

## Health Checks

### Backend
- Health endpoint: `http://localhost:8000/health`
- Check interval: 30s
- Timeout: 10s
- Retries: 3

### Database
- Check: `pg_isready`
- Check interval: 10s (main), 5s (test)
- Timeout: 5s (main), 3s (test)

## Troubleshooting

### Backend won't start
1. Check database is running: `make logs-db`
2. Verify environment variables: `cat backend/.env`
3. Check health endpoint: `curl http://localhost:8000/health`

### Frontend won't start
1. Check backend is running: `curl http://localhost:8000/health`
2. Verify environment variables: `cat frontend/.env.local`
3. Check logs: `make logs-frontend`

### Tests fail
1. **Backend**: Ensure test database is running (`make test-db-setup`)
2. **Frontend**: Install Playwright browsers (`make test-install-browsers`)
3. Check test logs for specific errors

### Port conflicts
- Backend: Change `BACKEND_PORT` in `.env`
- Frontend: Change `FRONTEND_PORT` in `.env.local`
- Database: Change `POSTGRES_PORT` in `.env`

## Best Practices

1. **Use Makefiles**: Always use Makefile commands for consistency
2. **Environment Variables**: Use `.env` files (not hardcoded)
3. **Volume Mounts**: Source code mounted for hot-reload in development
4. **Test Isolation**: Test database separate from development database
5. **Independent Projects**: Each project can run independently

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Docker Tests

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

## Project Independence

Both projects are designed to be **completely independent**:

- **Separate Dockerfiles**: Each project has its own Dockerfile
- **Separate docker-compose.yml**: Each project can run standalone
- **Separate Makefiles**: Each project has its own commands
- **No shared code**: No code dependencies between projects
- **Separate test frameworks**: Backend (pytest) and Frontend (Playwright/Vitest)

This allows:
- Moving projects to separate repositories
- Deploying independently
- Different teams working on each project
- Different deployment schedules

