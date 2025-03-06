from dataclasses import dataclass
from typing import Protocol

class CalculatorAPI(Protocol):
    def add(self, a: int, b: int) -> int:
        """Add two integers.

        Args:
            a: First integer
            b: Second integer

        Returns:
            Sum of a and b
        """
        ...

    def subtract(self, a: int, b: int) -> int:
        """Subtract second integer from first.

        Args:
            a: First integer
            b: Second integer

        Returns:
            Difference of a and b
        """
        ...

    def multiply(self, a: int, b: int) -> int:
        """Multiply two integers.

        Args:
            a: First integer
            b: Second integer

        Returns:
            Product of a and b
        """
        ...

@dataclass
class Calculator:
    """Calculator implementation that performs basic arithmetic operations."""

    def add(self, a: int, b: int) -> int:
        return a + b

    def subtract(self, a: int, b: int) -> int:
        return a - b

    def multiply(self, a: int, b: int) -> int:
        return a * b
