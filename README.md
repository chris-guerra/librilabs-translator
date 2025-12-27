# librilabs-translator-v2

Monorepo containing the frontend and backend applications for Librilabs Translator.

## Project Structure

This repository contains two independent projects:

- **`frontend/`** - Next.js 16.0.4 web application
- **`backend/`** - FastAPI (Python 3.14) backend application (to be created)

Each project is completely independent and can be copied/moved separately if needed.

## Architecture

The project follows a fullstack monolith architecture with modular design:

- **Platform:** Railway (hosting, database, CI/CD)
- **API Versioning:** All endpoints use `/api/v1/` prefix
- **Frontend:** Next.js 16.0.4 with React 19, TypeScript, Untitled UI components
- **Backend:** FastAPI monolith with extractable service modules
- **Database:** PostgreSQL (Railway managed) with SQLAlchemy 2.0
- **External Services:** OpenAI API (translation), Resend (post-MVP authentication)

For complete architecture details, see [docs/architecture.md](./docs/architecture.md).

## Getting Started

### Docker Development Setup (Recommended)

The easiest way to get started is using Docker Compose, which sets up all services (frontend, backend, and PostgreSQL) with a single command.

#### Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- Make (optional, but recommended for easier command execution)

#### Quick Start

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <repository-url>
   cd librilabs-translator-v2
   ```

2. **Set up environment variables**:
   ```bash
   # Backend environment variables
   cd backend
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   cd ..
   
   # Frontend environment variables
   cd frontend
   cp .env.example .env.local
   # Edit .env.local if you need to change the API URL
   cd ..
   ```

3. **Start all services**:
   ```bash
   make up-dev
   # Or: docker compose up -d
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Backend Health Check: http://localhost:8000/health
   - API Documentation: http://localhost:8000/docs

#### Development Modes

This project supports three development modes:

1. **Full-Stack Development** (root directory) - All services together
2. **Backend-Only Development** (`backend/` directory) - Backend + PostgreSQL
3. **Frontend-Only Development** (`frontend/` directory) - Frontend only (requires backend API running)

#### Makefile Commands

**Full-Stack Commands** (from project root):
- `make build` - Build all Docker images
- `make up` - Start all services in detached mode
- `make up-dev` - Start services with volume mounting for hot-reload (recommended for development)
- `make down` - Stop and remove all containers
- `make logs` - View logs from all services
- `make logs-backend` - View backend logs only
- `make logs-frontend` - View frontend logs only
- `make logs-db` - View database logs only
- `make restart` - Restart all services
- `make ps` - Show running containers
- `make clean` - Remove containers, volumes, and images (⚠️ This will delete all data)
- `make backend-<command>` - Run backend-specific commands (e.g., `make backend-up-dev`)
- `make frontend-<command>` - Run frontend-specific commands (e.g., `make frontend-up-dev`)

**Backend-Only Commands** (from `backend/` directory):
```bash
cd backend
make help        # Show all available commands
make build       # Build backend Docker image
make up-dev      # Start backend + PostgreSQL with hot-reload
make logs        # View backend and database logs
make test        # Run backend tests
```

**Frontend-Only Commands** (from `frontend/` directory):
```bash
cd frontend
make help        # Show all available commands
make build       # Build frontend Docker image
make up-dev      # Start frontend with hot-reload
make logs        # View frontend logs
make test        # Run frontend unit tests
make test-e2e    # Run frontend E2E tests
```

> **Note:** Each project (`backend/` and `frontend/`) has its own `docker-compose.yml` and `Makefile`, making them completely independent. This allows the projects to be split into separate repositories later without any changes.

#### Development Workflow

**Hot-Reload Development:**
- Both frontend and backend support hot-reload when using `make up-dev`
- Code changes are automatically reflected in running containers
- Frontend: Changes to files in `frontend/` trigger Next.js hot-reload
- Backend: Changes to files in `backend/` trigger uvicorn auto-reload

**Viewing Logs:**
```bash
# All services
make logs

# Specific service
make logs-backend
make logs-frontend
make logs-db
```

**Stopping Services:**
```bash
make down
```

**Rebuilding After Dependency Changes:**
```bash
# If you change requirements.txt or package.json
make build
make up-dev
```

#### Environment Variables

Each project (backend and frontend) has its own environment variable files, allowing them to be independent projects that can be split later.

**Backend Environment Variables** (`backend/.env`):
```bash
cd backend
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

> **Note:** The `.env` file is primarily for local development without Docker. When using Docker Compose, environment variables are set in `docker-compose.yml` with defaults. The `backend/.env` file will be loaded by Docker Compose if it exists, but is not required.

Required variables:
- `OPENAI_API_KEY` - Your OpenAI API key for translation services

Optional variables:
- `ALLOWED_ORIGINS` - CORS allowed origins (default: http://localhost:3000)
- `DATABASE_URL` - Database connection string (only needed for local development without Docker)

**Frontend Environment Variables** (`frontend/.env.local`):
```bash
cd frontend
cp .env.example .env.local
# Edit .env.local if you need to change the API URL
```

> **Note:** The `.env.local` file is primarily for local development without Docker. When using Docker Compose, environment variables are set in `docker-compose.yml` with defaults. The `frontend/.env.local` file will be loaded by Docker Compose if it exists, but is not required.

Optional variables:
- `NEXT_PUBLIC_API_URL` - Frontend API URL (default: http://localhost:8000)

**Docker Compose Environment Variables** (for docker-compose.yml):
These can be set in a root-level `.env` file or as environment variables:
- `POSTGRES_USER` - PostgreSQL username (default: librilabs)
- `POSTGRES_PASSWORD` - PostgreSQL password (default: librilabs_dev)
- `POSTGRES_DB` - Database name (default: librilabs_translator)
- `POSTGRES_PORT` - PostgreSQL port (default: 5432)
- `BACKEND_PORT` - Backend port (default: 8000)
- `FRONTEND_PORT` - Frontend port (default: 3000)

#### Troubleshooting

**Port Already in Use:**
If you get port conflict errors, either:
- Stop the conflicting service
- Change the port in `.env` file

**Permission Errors (Frontend):**
If you encounter permission errors with `.next` directory:
```bash
make down
make clean
make build
make up-dev
```

**Database Connection Issues:**
- Ensure PostgreSQL container is healthy: `make ps`
- Check database logs: `make logs-db`
- Verify DATABASE_URL in `.env` matches docker-compose.yml configuration

**Container Won't Start:**
- Check logs: `make logs`
- Rebuild images: `make build`
- Clean and restart: `make clean && make build && make up-dev`

**Hot-Reload Not Working:**
- Ensure you're using `make up-dev` (not `make up`)
- Check that volumes are mounted: `docker compose ps`
- Verify file permissions in mounted directories

### Independent Project Development

Each project can be developed independently:

**Backend Development:**
```bash
cd backend
cp .env.example .env
# Edit .env with your OPENAI_API_KEY
make up-dev
# Backend runs on http://localhost:8000
# PostgreSQL runs on localhost:5432
```

**Frontend Development:**
```bash
cd frontend
cp .env.example .env.local
# Edit .env.local if needed
make up-dev
# Frontend runs on http://localhost:3000
# Note: Backend API should be running (either via root docker-compose.yml or backend/docker-compose.yml)
```

### Local Development (Without Docker)

### Frontend

See [frontend/README.md](./frontend/README.md) for frontend setup instructions.

### Backend

See [backend/README.md](./backend/README.md) for backend setup instructions.

## Production Deployment

### Deployment Strategy

This project is designed for deployment on **Railway** (as specified in the architecture), but the Docker configuration supports deployment to any container orchestration platform.

#### Railway Deployment

**Recommended Approach:**
1. **Backend Service:**
   - Connect GitHub repository to Railway
   - Set root directory to `backend/`
   - Railway will automatically detect `backend/Dockerfile`
   - Configure environment variables in Railway dashboard:
     - `OPENAI_API_KEY` (required)
     - `DATABASE_URL` (provided by Railway PostgreSQL service)
     - `ALLOWED_ORIGINS` (your production frontend URL)
   - Railway will handle container builds and deployments automatically

2. **Frontend Service:**
   - Create separate Railway service for frontend
   - Set root directory to `frontend/`
   - Railway will automatically detect `frontend/Dockerfile`
   - Configure environment variables:
     - `NEXT_PUBLIC_API_URL` (your production backend URL)
   - For production, Railway will use the `runtime` stage from Dockerfile

3. **PostgreSQL Database:**
   - Create PostgreSQL service in Railway
   - Railway provides `DATABASE_URL` automatically to connected services
   - No manual configuration needed

**Production Docker Compose Considerations:**
- The provided `docker-compose.yml` files are optimized for **development**
- For production, consider:
  - Removing volume mounts (use built images)
  - Using production Dockerfile targets (`runtime` for frontend)
  - Setting `restart: unless-stopped` (already added)
  - Using secrets management instead of environment variables
  - Implementing resource limits
  - Using production-grade reverse proxy (nginx/traefik)

#### Production Dockerfile Targets

**Backend:**
- Uses multi-stage build (already optimized)
- Production-ready as-is

**Frontend:**
- Development: Uses `development` target (hot-reload)
- Production: Uses `runtime` target (optimized build)
- To use production target, update docker-compose.yml:
  ```yaml
  build:
    target: runtime  # instead of development
  ```

#### Container Restart Policies

All services in docker-compose.yml files include `restart: unless-stopped`:
- Containers automatically restart on failure
- Containers won't restart if manually stopped
- Suitable for both development and production environments

#### Security Considerations for Production

1. **Environment Variables:**
   - Never commit `.env` files
   - Use Railway's environment variable management
   - Rotate secrets regularly

2. **Secrets Detection:**
   - Pre-commit hooks configured with `detect-secrets` (see `backend/.pre-commit-config.yaml`)
   - To enable:
     ```bash
     cd backend
     pip install pre-commit detect-secrets
     detect-secrets scan > .secrets.baseline  # First time only
     pre-commit install
     ```
   - Baseline file: `backend/.secrets.baseline` (already exists)
   - Hooks will automatically scan for secrets before each commit

3. **Image Security:**
   - Regularly scan images: `docker scout cves <image-name>`
   - Keep base images updated
   - Review security advisories

4. **Network Security:**
   - Use Railway's built-in HTTPS/TLS
   - Configure CORS properly (`ALLOWED_ORIGINS`)
   - Don't expose database ports publicly

#### Monitoring and Observability

For production, consider:
- Railway's built-in metrics and logs
- Application performance monitoring (APM)
- Error tracking (e.g., Sentry)
- Health check endpoints (already implemented at `/health`)

#### Scaling

**Horizontal Scaling:**
- Backend: Stateless design supports multiple instances
- Frontend: Can be scaled independently
- Database: Use Railway's managed PostgreSQL (handles scaling)

**Vertical Scaling:**
- Adjust Railway service resources as needed
- Monitor resource usage in Railway dashboard

## Development Tools

### BMad Method

This project uses [BMad Method](https://github.com/bmad-method/bmad-method) (v4.44.3) - a universal AI agent framework for project management and documentation.

**Installation:**
```bash
npx bmad-method install
```

**Configuration:**
- PRD (Product Requirements Document) is sharded into multiple files
- Architecture documentation is sharded into multiple files
- No IDE integration configured (can be added manually if needed)

**Documentation:**
- User guide: `.bmad-core/user-guide.md`
- Framework files: `.bmad-core/` directory

For more information about the BMad workflow and how to use the agents effectively, refer to the user guide.