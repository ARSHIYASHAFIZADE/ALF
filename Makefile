.PHONY: dev up down build logs test clean

dev:
	docker compose up --build

up:
	docker compose up -d --build

down:
	docker compose down

build:
	docker compose build --no-cache

logs:
	docker compose logs -f

logs-backend:
	docker compose logs -f api worker

logs-frontend:
	docker compose logs -f frontend

test-backend:
	docker compose exec api pytest tests/ -v

test-frontend:
	docker compose exec frontend npm test

shell-backend:
	docker compose exec api bash

shell-frontend:
	docker compose exec frontend sh

redis-cli:
	docker compose exec redis redis-cli

clean:
	docker compose down -v --remove-orphans

# Local dev (without Docker)
dev-frontend:
	cd frontend && npm run dev

dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000
