.PHONY: help run install lint format clean

# Help command to list available Makefile operations
help:
	@echo "Available commands:"
	@echo "  make run         - Launch the FastAPI development server with hot reload using Uvicorn"
	@echo "  make install     - Install project dependencies via Poetry and setup git pre-commit hooks"
	@echo "  make lint        - Run strict linter and validation checks on all codebase files"
	@echo "  make format      - Auto-format Python files to adhere to strict coding styles"
	@echo "  make clean       - Clean temporary directories, bytecode, and Ruff cache files"

# Launch uvicorn server
run:
	poetry run uvicorn src.main:app --host 127.0.0.1 --port 9211 --reload

# Install poetry dependencies and precommit hooks
install:
	poetry install
	poetry run pre-commit install

# Lint all files using precommit validations
lint:
	poetry run pre-commit run --all-files

# Force formatting across the codebase
format:
	poetry run pre-commit run --all-files

# Clean project caches
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
