## Makefile for Project Chimera (infra)
## Usage (from project root):
##   make -f infra/Makefile <target>
## Targets:
##   setup       - Sync all dependencies (including dev) with uv
##   test        - Run test suite with pytest
##   lint        - Run ruff lint checks
##   format      - Auto-format code with ruff
##   type-check  - Run mypy static type checks
##   help        - Show this help message

.PHONY: help setup test lint format type-check

PROJECT_ROOT := $(abspath $(CURDIR))

setup:
	cd $(PROJECT_ROOT) && uv sync --dev

test:
	cd $(PROJECT_ROOT) && pytest

lint:
	cd $(PROJECT_ROOT) && ruff check .

format:
	cd $(PROJECT_ROOT) && ruff format .

type-check:
	cd $(PROJECT_ROOT) && mypy .

help:
	@echo "Available targets (run from project root with: make -f infra/Makefile <target>):"
	@echo "  setup       - Sync all dependencies (including dev) with uv"
	@echo "  test        - Run test suite with pytest"
	@echo "  lint        - Run ruff lint checks"
	@echo "  format      - Auto-format code with ruff"
	@echo "  type-check  - Run mypy static type checks"
