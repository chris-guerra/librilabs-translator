.PHONY: help build up up-dev down logs logs-backend logs-frontend logs-db clean restart ps backend frontend

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
	@echo "Project-Specific Commands:"
	@echo "  make backend        - Run backend commands (use: make backend help)"
	@echo "  make frontend       - Run frontend commands (use: make frontend help)"

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

