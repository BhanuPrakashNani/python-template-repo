# Component Documentation

This document describes the components available in this template and their usage. Each component is a separate UV package with its own dependencies and configuration.

## Directory Structure

```
src/
└── components/
    ├── calculator/              # Calculator component
    │   ├── pyproject.toml      # UV package config
    │   ├── __init__.py         # Public API
    │   ├── calculator.py       # Implementation
    │   └── tests/             # Unit tests
    │       └── test_calculator.py
    ├── logger/                 # Logger component
    │   ├── pyproject.toml
    │   ├── __init__.py
    │   ├── logger.py
    │   └── tests/
    │       └── test_logger.py
    └── notifier/              # Notifier component
        ├── pyproject.toml
        ├── __init__.py
        ├── notifier.py
        └── tests/
            └── test_notifier.py
```

## Components

### 1. Calculator

#### API
```python
from src.components.calculator import Calculator

calc = Calculator()
result = calc.add(1, 2)      # Returns: 3
result = calc.subtract(5, 3)  # Returns: 2
result = calc.multiply(2, 3)  # Returns: 6
```

#### Methods
- `add(a: int, b: int) -> int`: Add two integers
- `subtract(a: int, b: int) -> int`: Subtract second number from first
- `multiply(a: int, b: int) -> int`: Multiply two integers

### 2. Logger

#### API
```python
from src.components.logger import Logger

logger = Logger()
logger.log("Operation completed")  # Prints: LOG: Operation completed
```

#### Methods
- `log(message: str) -> None`: Log a message to console

### 3. Notifier

#### API
```python
from src.components.notifier import Notifier

notifier = Notifier()
notifier.notify("Alert!")  # Prints: NOTIFICATION: Alert!
```

#### Methods
- `notify(message: str) -> None`: Send a notification message

## Testing

Each component includes:
1. Unit tests located next to the component code
2. Integration tests in the top-level tests/Integration directory
3. End-to-end tests in the top-level tests/EndToEnd directory

### Running Component Tests

To run tests for a specific component:
```bash
pytest src/components/calculator/tests  # Run calculator tests
pytest src/components/logger/tests      # Run logger tests
pytest src/components/notifier/tests    # Run notifier tests
```

To run integration tests:
```bash
pytest tests/Integration
```

To run end-to-end tests:
```bash
pytest tests/EndToEnd
```

## Component Development

### Creating a New Component

1. Create a new directory under src/components
2. Add pyproject.toml for UV package configuration
3. Create __init__.py with public API definitions
4. Add implementation files
5. Create tests directory with component tests

### Example Component Structure
```
my_component/
├── pyproject.toml
├── __init__.py
├── my_component.py
└── tests/
    ├── __init__.py
    └── test_my_component.py
