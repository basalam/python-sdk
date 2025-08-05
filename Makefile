.PHONY: install install-dev clean lint test build publish check
.DEFAULT_GOAL := help

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "%-12s %s\n", $$1, $$2}'

install: ## Install package
	pip install -e .

install-dev: ## Install with dev dependencies
	pip install -e ".[dev,lint,test]"

clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/ htmlcov/
	find . -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete

lint: ## Run code quality checks
	black --check src/ tests/
	isort --check-only src/ tests/
	ruff check src/ tests/
	mypy src/

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=basalam_sdk --cov-report=xml --cov-report=term-missing

check: ## Run all quality checks
	make lint
	make test

build: ## Build package
	python3 -m build

publish: ## Publish to PyPI
	@if [ -z "$(PYPI_TOKEN)" ]; then \
		echo "Error: PYPI_TOKEN environment variable is required"; \
		exit 1; \
	fi
	python -m twine upload dist/* --username __token__ --password $(PYPI_TOKEN)

publish-test: ## Publish to Test PyPI
	@if [ -z "$(TEST_PYPI_TOKEN)" ]; then \
		echo "Error: TEST_PYPI_TOKEN environment variable is required"; \
		exit 1; \
	fi
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* --username __token__ --password $(TEST_PYPI_TOKEN)

release: clean generate-stubs build publish ## Complete release process (clean, build, publish)

release-test: clean generate-stubs build publish-test ## Complete test release process (clean, build, publish to test PyPI)

generate-stubs: ## Generate type stubs for IDE autocomplete
	python3 scripts/generate_stubs.py 