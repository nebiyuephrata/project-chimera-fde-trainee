.PHONY: help install lint fmt test

help:
	@echo "Targets:"
	@echo "  install  - install dev dependencies"
	@echo "  lint     - run ruff"
	@echo "  fmt      - run black"
	@echo "  test     - run pytest"

install:
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

lint:
	ruff check .

fmt:
	black .

test:
	pytest -q

