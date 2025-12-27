# Development Workflow

Development setup and workflow for the fullstack application.

## Local Development Setup

### Prerequisites

```bash
# Required software
- Node.js 18+ and npm
- Python (latest stable version)
- Docker and Docker Compose
- Git
```

### Initial Setup

```bash
# Clone repository
git clone <repository-url>
cd librilabs-translator-v2

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
cp frontend/.env.local.example frontend/.env.local
cp backend/.env.example backend/.env

# Edit .env files with your configuration:
# - DATABASE_URL (for backend)
# - OPENAI_API_KEY (for backend) - See OpenAI API Key Setup below
# - NEXT_PUBLIC_API_URL (for frontend)

# OpenAI API Key Setup:
# 1. Create an account at https://platform.openai.com
# 2. Navigate to API Keys section in your account settings
# 3. Generate a new API key (starts with 'sk-')
# 4. Copy the key and add it to backend/.env as OPENAI_API_KEY=sk-...
# 5. Note: API keys have usage limits based on your account tier
#    - Default tier: ~3,500 requests/minute, ~90,000 tokens/minute
#    - Monitor usage in OpenAI dashboard to avoid quota exhaustion
# 6. Never commit API keys to version control - use .env.example as template only

# OpenAI API Offline Development Mode:
# For local development when OpenAI API is unavailable (rate limits, network issues, or cost concerns):
# 1. Set environment variable: USE_MOCK_OPENAI=true in backend/.env
# 2. Translation service will use mock responses instead of real API calls
# 3. Mock responses return deterministic translations based on input text
#    - Simple pattern: "Translated: {original_text}" for testing
#    - Preserves paragraph structure and chunking behavior
#    - Simulates API response format for realistic testing
# 4. Mock mode allows full workflow testing without API costs or rate limits
# 5. Production deployments must have USE_MOCK_OPENAI=false or unset (enforced by environment check)

# Start all services with Docker Compose (using Makefile)
make up-dev

# Or using Docker Compose directly:
# docker-compose up -d

# Or start services individually:
# Backend: cd backend && uvicorn app.main:app --reload
# Frontend: cd frontend && npm run dev
# Database: docker-compose up postgres
```

### Development Commands

**Using Makefile (Recommended):**
```bash
# Build all Docker images
make build

# Start all services in development mode (with hot-reload)
make up-dev

# Start all services in detached mode
make up

# Stop all services
make down

# View logs from all services
make logs

# View logs from specific service
make logs-backend
make logs-frontend
make logs-db

# Restart all services
make restart

# Show running containers
make ps

# Clean up (remove containers, volumes, and images)
make clean
```

**Using npm scripts:**
```bash
# Start all services
npm run dev

# Start frontend only
cd frontend && npm run dev

# Start backend only
cd backend && uvicorn app.main:app --reload

# Run tests
npm run test

# Run linting
npm run lint
```

**Database Migrations:**
```bash
# Run database migrations (from within backend container or locally)
make exec-backend alembic upgrade head

# Or if running locally:
cd backend && alembic upgrade head

# Create new migration
cd backend && alembic revision --autogenerate -m "description"
```

## Environment Configuration

### Required Environment Variables

```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend (.env)
# For Docker Compose (local development):
DATABASE_URL=postgresql+asyncpg://librilabs:librilabs_dev@postgres:5432/librilabs_translator
# For local PostgreSQL (without Docker):
# DATABASE_URL=postgresql+asyncpg://librilabs:librilabs_dev@localhost:5432/librilabs_translator
OPENAI_API_KEY=sk-...
RESEND_API_KEY=re_...  # Post-MVP
JWT_SECRET=...  # Post-MVP
ENVIRONMENT=development

# Shared
SESSION_SECRET=...  # For session management
```

---
