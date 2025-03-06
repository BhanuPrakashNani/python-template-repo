# Python Template Repository

A template repository demonstrating Python best practices with UV package management, component-based architecture, and comprehensive testing.

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/BhanuPrakashNani/python-template-repo/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/BhanuPrakashNani/python-template-repo/tree/main)

## Features

- **Modern Package Management**: Uses [UV](https://github.com/astral-sh/uv) for fast, reliable Python package management
- **Component Architecture**: Modular design with each component as a separate UV package
- **Comprehensive Testing**: Unit tests with each component, plus integration and E2E tests
- **Code Quality**: Ruff for linting/formatting and Mypy for type checking
- **CI/CD**: Automated testing and quality checks with CircleCI

## Project Structure

```
python-template-repo/
├── src/
│   └── components/          # Each component is a UV package
│       ├── calculator/
│       ├── logger/
│       └── notifier/
├── tests/
│   ├── Integration/        # Integration tests
│   └── EndToEnd/          # End-to-end tests
├── pyproject.toml         # Project configuration
└── components.md         # Component documentation
```

## Prerequisites

- Python 3.11 or higher
- UV package manager

## Installation

1. Install UV package manager:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/python-template-repo.git
   cd python-template-repo
   ```

3. Create virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. Install components in development mode:
   ```bash
   uv pip install -e src/components/calculator
   uv pip install -e src/components/logger
   uv pip install -e src/components/notifier
   ```

## Usage

See [components.md](components.md) for detailed component documentation and APIs.

### Running Tests

1. Run unit tests for a specific component:
   ```bash
   pytest src/components/calculator/tests
   pytest src/components/logger/tests
   pytest src/components/notifier/tests
   ```

2. Run all unit tests:
   ```bash
   pytest src/components/*/tests
   ```

3. Run integration tests:
   ```bash
   pytest tests/Integration
   ```

4. Run end-to-end tests:
   ```bash
   pytest tests/EndToEnd
   ```

5. Run all tests with coverage:
   ```bash
   pytest --cov=src --cov-report=html
   ```

### Code Quality

1. Run linting:
   ```bash
   ruff check .
   ```

2. Run type checking:
   ```bash
   mypy src/components/*/src
   ```

## CI/CD Pipeline

This repository uses CircleCI for continuous integration and deployment:

- **Build Status**: [![CircleCI](https://dl.circleci.com/status-badge/img/gh/BhanuPrakashNani/python-template-repo/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/BhanuPrakashNani/python-template-repo/tree/main)

The pipeline:
1. Installs UV and project dependencies
2. Runs linting and type checking
3. Executes unit, integration, and E2E tests
4. Generates coverage reports

Example builds:
- [Passed Build](https://app.circleci.com/pipelines/github/BhanuPrakashNani/python-template-repo/latest/passing)
- [Failed Build](https://app.circleci.com/pipelines/github/BhanuPrakashNani/python-template-repo/latest/failing)
- [Coverage Report](https://app.circleci.com/pipelines/github/BhanuPrakashNani/python-template-repo/latest/artifacts)

## Creating New Components

1. Create component structure:
   ```
   src/components/my_component/
   ├── pyproject.toml
   ├── __init__.py
   ├── my_component.py
   └── tests/
       ├── __init__.py
       └── test_my_component.py
   ```

2. Add UV package configuration in pyproject.toml
3. Define public API in __init__.py
4. Implement component functionality
5. Add unit tests

See [components.md](components.md) for detailed instructions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
