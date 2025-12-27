.PHONY: help build up up-dev down logs logs-backend logs-frontend logs-db clean restart ps backend frontend test test-backend test-frontend test-e2e

# Default target
help:
	@echo "Full-Stack Development Commands:"
	@echo "  make build          - Build all Docker images"
	@echo "  make up             - Start all services in detached mode"
	@echo "  make up-dev         - Start services with volume mounting for hot-reload"
	@echo "  make down           - Stop and remove all containers"
	@echo "  make logs           - View logs from all services"
	@echo "  make logs-backend   - View backend logs only"
	@echo "  make logs-frontend  - View frontend logs only"
	@echo "  make logs-db        - View database logs only"
	@echo "  make clean          - Remove containers, volumes, and images"
	@echo "  make restart        - Restart all services"
	@echo "  make ps             - Show running containers"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test           - Run all tests (backend + frontend)"
	@echo "  make test-backend   - Run backend tests only"
	@echo "  make test-frontend  - Run frontend unit tests only"
	@echo "  make test-e2e       - Run frontend E2E tests only"
	@echo ""
	@echo "Project-Specific Commands:"
	@echo "  make backend <cmd>  - Run backend commands (e.g., make backend test)"
	@echo "  make frontend <cmd> - Run frontend commands (e.g., make frontend test)"

# Build all Docker images
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
	docker compose logs -f librilabs-translator-backend

# View frontend logs only
logs-frontend:
	docker compose logs -f librilabs-translator-frontend

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

# Delegate to backend Makefile
# Usage: make backend <command>, e.g., make backend up-dev
backend-%:
	@cd backend && $(MAKE) $(subst backend-,,$@)

# Delegate to frontend Makefile
# Usage: make frontend <command>, e.g., make frontend up-dev
frontend-%:
	@cd frontend && $(MAKE) $(subst frontend-,,$@)

# Run all tests
test: test-backend test-frontend
	@echo "All tests completed!"

# Run backend tests
test-backend:
	@echo "Running backend tests..."
	@cd backend && $(MAKE) test

# Run frontend unit tests
test-frontend:
	@echo "Running frontend unit tests..."
	@cd frontend && $(MAKE) test

# Run frontend E2E tests
test-e2e:
	@echo "Running frontend E2E tests..."
	@cd frontend && $(MAKE) test-e2e

