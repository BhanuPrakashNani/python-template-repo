# Python Template Repository

A template for creating modular Python projects with component-based architecture, proper API definitions, and comprehensive testing.

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/Loke7132/python-template-repo/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/Loke7132/python-template-repo/tree/main)

[View Test Results and Coverage on CircleCI](https://app.circleci.com/pipelines/github/Loke7132/python-template-repo)

## CI/CD Status

- **Test Results**: View all test runs in [CircleCI Dashboard](https://app.circleci.com/pipelines/github/Loke7132/python-template-repo)
  - Unit Tests: See individual component test results
  - Integration Tests: Component interaction verification
  - E2E Tests: Complete workflow validation
- **Code Coverage**: Available in test artifacts for each build
- **Build History**: Track all builds and their status

## Features

- **Component-Based Architecture**: Each component is an independent UV package
- **Strong API Design**: Clear protocols and implementations
- **Modern Python Tooling**: UV for dependency management, pytest for testing
- **Co-located Tests**: Unit tests near component code
- **Multiple Test Levels**: Unit, integration, and E2E tests
- **Clean Project Structure**: Clear organization and separation of concerns
- **Continuous Integration**: Automated testing and coverage reporting

## Project Structure

```
python-template-repo/
├── src/
│   └── components/          # Each component is a UV package
│       ├── calculator/
│       │   ├── __init__.py  # Exports component API
│       │   ├── api.py       # Protocol + Implementation
│       │   ├── tests/       # Component's unit tests
│       │   └── pyproject.toml
│       ├── logger/
│       └── notifier/
├── tests/                   # Project-level tests
│   ├── integration/        # Component interaction tests
│   └── e2e/               # End-to-end workflows
├── .circleci/              # CI/CD configuration
├── components.md           # Component architecture docs
├── pyproject.toml         # Project configuration
└── README.md
```

## Getting Started

### Prerequisites

The only prerequisite is UV, which is used for dependency management:

```bash
# Install UV (higher level than Python, no pip needed)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Loke7132/python-template-repo.git
   cd python-template-repo
   ```

2. Install the project and its dependencies using UV:
   ```bash
   uv pip install -e ".[test]"
   ```

## Running Tests

The project uses pytest and supports multiple levels of testing:

### Unit Tests

Run tests for a specific component:
```bash
# Test calculator component
pytest src/components/calculator/tests/

# Test logger component
pytest src/components/logger/tests/

# Test notifier component
pytest src/components/notifier/tests/
```

Run a specific test file:
```bash
pytest src/components/calculator/tests/test_calculator.py
```

Run a specific test case:
```bash
pytest src/components/calculator/tests/test_calculator.py::test_add
```

### Integration Tests

Test how components work together:
```bash
pytest tests/integration/
```

### End-to-End Tests

Test complete workflows:
```bash
pytest tests/e2e/
```

### All Tests

Run all tests with coverage:
```bash
pytest --cov=src
```

## Development

For details on the component architecture, see [components.md](components.md).

### Adding a New Component

1. Create component structure:
   ```bash
   mkdir -p src/components/new_component/{tests,__pycache__}
   ```

2. Create required files:
   ```bash
   # API definition and implementation
   touch src/components/new_component/api.py
   
   # Package exports
   touch src/components/new_component/__init__.py
   
   # UV package config
   touch src/components/new_component/pyproject.toml
   
   # Unit tests
   touch src/components/new_component/tests/test_new_component.py
   ```

3. Update root pyproject.toml to include the new component.

### Code Quality

Format code:
```bash
ruff format .
```

Run linter:
```bash
ruff check .
```

Type checking:
```bash
mypy .
```

## Learn More

- [Component Architecture](components.md): Detailed explanation of the component-based design
- [UV Documentation](https://github.com/astral-sh/uv): Modern Python package management
- [pytest Documentation](https://docs.pytest.org/): Python testing framework
- [CircleCI Dashboard](https://app.circleci.com/pipelines/github/Loke7132/python-template-repo): CI/CD status and test results
