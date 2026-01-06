.PHONY: help setup lint format test run clean demo-log

help:
	@echo "make setup   - install deps"
	@echo "make lint    - ruff check"
	@echo "make format  - ruff format"
	@echo "make test    - pytest"
	@echo "make run     - run entrypoint"
	@echo "make demo-log - run with logging demo"
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
	@uv run python -m security_automation

demo-log:
	@LOG_LEVEL=INFO uv run python -m security_automation

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov dist build *.egg-info
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \;
