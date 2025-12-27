.PHONY: help build up up-dev down logs logs-frontend clean restart ps test test-e2e

# Default target
help:
	@echo "Frontend Development Commands:"
	@echo "  make build          - Build Docker image"
	@echo "  make up             - Start frontend in detached mode"
	@echo "  make up-dev         - Start frontend with volume mounting for hot-reload"
	@echo "  make down           - Stop and remove container"
	@echo "  make logs           - View frontend logs"
	@echo "  make logs-frontend  - View frontend logs (alias for logs)"
	@echo "  make clean          - Remove container and image"
	@echo "  make restart        - Restart frontend"
	@echo "  make ps             - Show running containers"
	@echo "  make test           - Run unit tests"
	@echo "  make test-e2e       - Run end-to-end tests"

# Build Docker image
build:
	docker compose build

# Start frontend in detached mode
up:
	docker compose up -d

# Start frontend with volume mounting for hot-reload
up-dev:
	docker compose up -d

# Stop and remove container
down:
	docker compose down

# View frontend logs
logs:
	docker compose logs -f frontend

# View frontend logs (alias)
logs-frontend:
	docker compose logs -f frontend

# Remove container and image
clean:
	docker compose down -v --rmi all

# Restart frontend
restart:
	docker compose restart

# Show running containers
ps:
	docker compose ps

# Run unit tests
test:
	docker compose exec frontend npm test || docker compose run --rm frontend npm test

# Run end-to-end tests
test-e2e:
	docker compose exec frontend npm run test:e2e || docker compose run --rm frontend npm run test:e2e

