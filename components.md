# Components Documentation

This document provides an overview of the components in the `src/components/` directory. Each component is designed to perform a specific function and is thoroughly tested with unit, integration, and end-to-end tests.

---

## 1. **Calculator**

### Description
The `Calculator` component performs basic arithmetic operations such as addition, subtraction, and multiplication.

### Location
- File: `src/components/calculator.py`
- Class: `Calculator`

### Methods
- **`add(a: int, b: int) -> int`**  
  Adds two integers and returns the result.  
  Example: `calc.add(1, 2)` returns `3`.

- **`subtract(a: int, b: int) -> int`**  
  Subtracts the second integer from the first and returns the result.  
  Example: `calc.subtract(5, 3)` returns `2`.

- **`multiply(a: int, b: int) -> int`**  
  Multiplies two integers and returns the result.  
  Example: `calc.multiply(2, 3)` returns `6`.

### Unit Tests
- File: `tests/unit/test_calculator.py`
- Tests:
  - `test_addition`: Verifies the `add` method.
  - `test_subtraction`: Verifies the `subtract` method.
  - `test_multiplication`: Verifies the `multiply` method.

---

## 2. **Logger**

### Description
The `Logger` component records operations performed by the `Calculator` and stores them in a log.

### Location
- File: `src/components/logger.py`
- Class: `Logger`

### Methods
- **`log(message: str) -> None`**  
  Logs a message.  
  Example: `logger.log("Addition performed: 1 + 2 = 3")`.

### Unit Tests
- File: `tests/unit/test_logger.py`
- Tests:
  - `test_logger`: Verifies the `log` method.

---

## 3. **Notifier**

### Description
The `Notifier` component sends an alert when the result of a `Calculator` operation exceeds a given threshold.

### Location
- File: `src/components/notifier.py`
- Class: `Notifier`

### Methods
- **`notify(message: str) -> None`**  
  Sends a notification.  
  Example: `notifier.notify("Threshold exceeded: Result is 10")`.

### Unit Tests
- File: `tests/unit/test_notifier.py`
- Tests:
  - `test_notifier`: Verifies the `notify` method.

---

## Integration Tests

### Calculator + Logger
- File: `tests/Integration/test_calculator_logger_integration.py`
- Tests:
  - Verifies that `Calculator` operations are logged by the `Logger`.

### Logger + Notifier
- File: `tests/Integration/test_logger_notifier_integration.py`
- Tests:
  - Verifies that the `Logger` triggers the `Notifier` when a threshold is exceeded.

---

## End-to-End Tests

### Calculator → Logger → Notifier
- File: `tests/EndToEnd/test_e2e.py`
- Tests:
  - Verifies the entire workflow:  
    1. Perform a calculation using the `Calculator`.  
    2. Log the operation using the `Logger`.  
    3. Send a notification using the `Notifier` if the result exceeds a threshold.

---

## Usage Example

```python
from src.components.calculator import Calculator
from src.components.logger import Logger
from src.components.notifier import Notifier

# Initialize components
calc = Calculator()
logger = Logger()
notifier = Notifier()

# Perform a calculation
result = calc.add(1, 2)

# Log the operation
logger.log(f"Addition performed: 1 + 2 = {result}")

# Notify if the result exceeds a threshold
if result > 2:
    notifier.notify(f"Threshold exceeded: Result is {result}")
