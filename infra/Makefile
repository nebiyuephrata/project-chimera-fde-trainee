# Makefile for Project Chimera
# Run from project root: make <target>

.PHONY: help setup test lint format type-check spec-check demo mcp-demo redis-up frontend ws-mock db-up db-down api orchestrator-api hitl-smoke

help:
	@echo "Available targets:"
	@echo "  setup       - Install dependencies (uv sync --dev)"
	@echo "  test        - Run all tests with pytest"
	@echo "  lint        - Run Ruff lint checks"
	@echo "  format      - Auto-format code with Ruff"
	@echo "  type-check  - Run Mypy static type checking"
	@echo "  spec-check  - Placeholder for spec validation (TODO)"
	@echo "  demo        - Run the FastRender Swarm demo"
	@echo "  mcp-demo    - Run the FastRender Swarm demo with MCP mock"
	@echo "  redis-up    - Start Redis 7 via Docker"
	@echo "  frontend    - Build the React frontend"
	@echo "  ws-mock     - Run mock HITL WebSocket server"
	@echo "  db-up       - Start Orchestrator API + Redis/Postgres/Weaviate via Docker Compose"
	@echo "  db-down     - Stop Docker Compose services"
	@echo "  api         - Run HITL FastAPI server (local)"
	@echo "  orchestrator-api - Run Orchestrator Campaign API (local, Postgres-backed)"
	@echo "  hitl-smoke  - Run HITL API/WS smoke test"

setup:
	uv sync --dev

test:
	PYTHONPATH=. uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

type-check:
	uv run mypy .

spec-check:
	@echo "TODO: implement spec validation script"

demo:
	PYTHONPATH=. uv run python src/swarm/demo.py

mcp-demo:
	PYTHONPATH=. uv run python src/swarm/demo.py

redis-up:
	docker run --rm -p 6379:6379 redis:7

frontend:
	cd frontend && npm install && npm run build

ws-mock:
	PYTHONPATH=. uv run python src/swarm/ws_mock.py

db-up:
	docker compose -f infra/docker-compose.yml up -d

db-down:
	docker compose -f infra/docker-compose.yml down

api:
	PYTHONPATH=. uv run uvicorn src.api.hitl_api:app --reload --host 0.0.0.0 --port 8000

orchestrator-api:
	CHIMERA_CAMPAIGN_DB_BACKEND=postgres PYTHONPATH=. uv run uvicorn src.api.orchestrator_api:app --reload --host 0.0.0.0 --port 8001

hitl-smoke:
	PYTHONPATH=. uv run python scripts/hitl_smoke.py
