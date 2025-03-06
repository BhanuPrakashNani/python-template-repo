# Component Architecture

This document explains the component-based architecture used in this template.

## What is a Component?

A component is a self-contained module that:
1. Has a well-defined API (Protocol)
2. Implements specific functionality
3. Can be tested independently
4. Has its own dependencies
5. Is packaged as a separate UV package

## Component Structure

Each component follows this structure:
```
component_name/
├── __init__.py      # Exports the component's API
├── api.py           # Contains Protocol definition and implementation
├── tests/           # Co-located unit tests
│   └── test_*.py
└── pyproject.toml   # Component-specific UV package config
```

### Key Files Explained

1. **api.py**:
   - Defines the component's Protocol (interface)
   - Contains the implementation
   - Example:
   ```python
   from typing import Protocol
   
   class CalculatorAPI(Protocol):
       def add(self, a: int, b: int) -> int:
           """Add two numbers."""
           ...
   
   class Calculator:
       def add(self, a: int, b: int) -> int:
           return a + b
   ```

2. **__init__.py**:
   - Exports the public API
   - Example:
   ```python
   from .api import Calculator
   __all__ = ["Calculator"]
   ```

3. **pyproject.toml**:
   - Defines component as UV package
   - Specifies dependencies
   - Configures testing and linting
   - Example:
   ```toml
   [project]
   name = "calculator"
   version = "0.1.0"
   dependencies = []
   ```

4. **tests/**:
   - Contains unit tests
   - Co-located with component code
   - Follows pytest conventions

## Integration Between Components

Components can be used together while maintaining independence:

```python
from calculator import Calculator
from logger import Logger

calc = Calculator()
logger = Logger()

result = calc.add(1, 2)
logger.log(f"Result: {result}")
```

## Testing Levels

1. **Unit Tests** (in component/tests/):
   - Test component in isolation
   - Co-located with component code
   - Run with: `pytest src/components/calculator/tests/`

2. **Integration Tests** (in tests/integration/):
   - Test component interactions
   - Located at project root
   - Run with: `pytest tests/integration/`

3. **End-to-End Tests** (in tests/e2e/):
   - Test complete workflows
   - Located at project root
   - Run with: `pytest tests/e2e/`

## Adding New Components

To add a new component:

1. Create directory structure:
   ```bash
   mkdir -p src/components/new_component/{tests,__pycache__}
   ```

2. Create required files:
   - api.py with Protocol and implementation
   - __init__.py for exports
   - pyproject.toml for UV package
   - Unit tests in tests/

3. Update root pyproject.toml to include component:
   ```toml
   dependencies = [
       "new_component @ {root}/src/components/new_component"
   ]
   ```

## Best Practices

1. **API First**: Define Protocol before implementation
2. **Single Responsibility**: Each component does one thing well
3. **Independence**: Components should have minimal dependencies
4. **Co-located Tests**: Keep unit tests with component code
5. **Clear Boundaries**: Use Protocol to define component interface
