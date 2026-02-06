## Makefile for Project Chimera (infra)
## Usage:
##   Run from the project root with uv installed:
##     make -f infra/Makefile <target>
## Targets:
##   setup       - Sync all dependencies (including dev) with uv
##   test        - Run test suite with pytest
##   lint        - Run ruff lint checks
##   format      - Auto-format code with ruff
##   type-check  - Run mypy static type checks
##   spec-check  - Placeholder for spec validation script
##   help        - Show this help message

.PHONY: help setup test lint format type-check spec-check

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

spec-check:
	cd $(PROJECT_ROOT) && echo "TODO: implement spec validation script"

help:
	@echo "Available targets (run from project root with: make -f infra/Makefile <target>):"
	@echo "  setup       - Sync all dependencies (including dev) with uv"
	@echo "  test        - Run test suite with pytest"
	@echo "  lint        - Run ruff lint checks"
	@echo "  format      - Auto-format code with ruff"
	@echo "  type-check  - Run mypy static type checks"
	@echo "  spec-check  - Placeholder for spec validation script"
