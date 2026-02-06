# Makefile for Project Chimera
# Run from project root: make <target>

.PHONY: help setup test lint format type-check spec-check

help:
	@echo "Available targets:"
	@echo "  setup       - Install dependencies (uv sync --dev)"
	@echo "  test        - Run all tests with pytest"
	@echo "  lint        - Run Ruff lint checks"
	@echo "  format      - Auto-format code with Ruff"
	@echo "  type-check  - Run Mypy static type checking"
	@echo "  spec-check  - Placeholder for spec validation (TODO)"

setup:
	uv sync --dev

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

type-check:
	uv run mypy .

spec-check:
	@echo "TODO: implement spec validation script"