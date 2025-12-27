.PHONY: help build up up-dev down logs logs-backend logs-db clean restart ps test

# Default target
help:
	@echo "Backend Development Commands:"
	@echo "  make build          - Build Docker image"
	@echo "  make up             - Start backend and database in detached mode"
	@echo "  make up-dev         - Start services with volume mounting for hot-reload"
	@echo "  make down           - Stop and remove all containers"
	@echo "  make logs           - View logs from all services"
	@echo "  make logs-backend   - View backend logs only"
	@echo "  make logs-db        - View database logs only"
	@echo "  make clean          - Remove containers, volumes, and images"
	@echo "  make restart        - Restart all services"
	@echo "  make ps             - Show running containers"
	@echo "  make test           - Run tests"

# Build Docker image
build:
	docker compose build

# Start all services in detached mode
up:
	docker compose up -d

# Start services with volume mounting for hot-reload
up-dev:
	docker compose up -d

# Stop and remove all containers
down:
	docker compose down

# View logs from all services
logs:
	docker compose logs -f

# View backend logs only
logs-backend:
	docker compose logs -f backend

# View database logs only
logs-db:
	docker compose logs -f postgres

# Remove containers, volumes, and images
clean:
	docker compose down -v --rmi all

# Restart all services
restart:
	docker compose restart

# Show running containers
ps:
	docker compose ps

# Run tests
test:
	docker compose --profile test up -d postgres-test
	@echo "Waiting for test database to be ready..."
	@sleep 3
	docker compose exec backend pytest || docker compose run --rm backend pytest
	@docker compose --profile test down postgres-test

# Run tests with coverage
test-coverage:
	docker compose --profile test up -d postgres-test
	@echo "Waiting for test database to be ready..."
	@sleep 3
	docker compose exec backend pytest --cov=app --cov-report=html --cov-report=term || docker compose run --rm backend pytest --cov=app --cov-report=html --cov-report=term
	@docker compose --profile test down postgres-test

# Run specific test file
test-file:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make test-file FILE=tests/integration/test_routers/test_health.py"; \
		exit 1; \
	fi
	docker compose --profile test up -d postgres-test
	@echo "Waiting for test database to be ready..."
	@sleep 3
	docker compose exec backend pytest $(FILE) || docker compose run --rm backend pytest $(FILE)
	@docker compose --profile test down postgres-test

# Run tests in verbose mode
test-verbose:
	docker compose --profile test up -d postgres-test
	@echo "Waiting for test database to be ready..."
	@sleep 3
	docker compose exec backend pytest -v || docker compose run --rm backend pytest -v
	@docker compose --profile test down postgres-test

# Setup test database
test-db-setup:
	docker compose --profile test up -d postgres-test
	@echo "Test database is ready at localhost:5433"

