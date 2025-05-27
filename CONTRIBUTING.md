# Contributing to Basalam SDK for Python

We love your input! We want to make contributing to the Basalam SDK as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

To set up your local development environment:

```bash
# Clone your fork of the repo
git clone https://github.com/YOUR_USERNAME/python-sdk.git
cd python-sdk

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Code Style

This project follows these coding standards:

- We use `black` for code formatting
- We use `isort` for import sorting
- We use `ruff` for linting
- We use `mypy` for type checking

You can run all checks with:

```bash
black src tests
isort src tests
ruff src tests
mypy src
```

Or use pre-commit:

```bash
pre-commit install
git add .
git commit -m "Your message"
```

### Testing

Write tests for your code using `pytest`. Run tests with:

```bash
pytest
```

For coverage reporting:

```bash
pytest --cov=src/basalam_sdk tests/
```

## Adding New Services

When adding support for a new Basalam service, follow these steps:

1. Create a new service directory under `src/basalam_sdk/` with the service name (e.g., `payment/`)
2. Implement the service following the established pattern:
    - `__init__.py` - Export public classes and functions
    - `client.py` - Service client implementation extending BaseClient
    - `models.py` - Data models using dataclasses or pydantic
3. Follow the existing code style:
    - Provide both synchronous and asynchronous methods
    - Use strong typing with proper return types
    - Write comprehensive docstrings
    - Implement proper error handling
4. Add the service to the main `BasalamClient` class in `src/basalam_sdk/basalam_client.py`
5. Add tests for the new service in the `tests/` directory
6. Update documentation as needed

## Project Architecture

Please review the [Architecture Documentation](docs/architecture.md) to understand the project's structure and design
patterns before contributing.

## Backward Compatibility

This project takes backward compatibility seriously. Before making changes, please review
the [Versioning and Compatibility Guide](docs/versioning_and_compatibility.md).

Key points:

- Do not remove or rename public methods or classes
- Do not change method signatures in incompatible ways
- Use deprecation warnings before removing features
- Follow semantic versioning principles

## Documentation

When adding or modifying features, be sure to update the relevant documentation:

- Update docstrings in the code
- Update or add entries in the appropriate `.md` files in the `docs/` directory
- Add examples if appropriate

## Versioning

We use [Semantic Versioning](https://semver.org/) for versioning:

- Major version changes for incompatible API changes
- Minor version changes for new functionality in a backward-compatible manner
- Patch version changes for backward-compatible bug fixes

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License. 
