.PHONY: help setup lint format test run clean

help:
	@echo "make setup   - install deps"
	@echo "make lint    - ruff check"
	@echo "make format  - ruff format"
	@echo "make test    - pytest"
	@echo "make run     - run entrypoint"
	@echo "make clean   - remove caches"

setup:
	uv sync

lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format .

test:
	uv run pytest tests/ -v --cov=src

run:
	uv run python src/security_automation/main.py

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov dist build *.egg-info
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \;
