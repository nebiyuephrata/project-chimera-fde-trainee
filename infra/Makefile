# Makefile for Project Chimera
# Run from project root: make <target>

.PHONY: help setup test lint format type-check spec-check demo mcp-demo redis-up frontend ws-mock

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
