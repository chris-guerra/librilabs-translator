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
	docker compose exec backend pytest || docker compose run --rm backend pytest

