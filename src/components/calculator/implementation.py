from .api import CalculatorAPI

class Calculator:
    """Implementation of the Calculator component.
    
    This class provides basic arithmetic operations like addition,
    subtraction, and multiplication.
    """
    
    def add(self, a: int, b: int) -> int:
        """Add two integers.
        
        Args:
            a: First integer
            b: Second integer
            
        Returns:
            Sum of the two integers
        """
        return a + b

    def subtract(self, a: int, b: int) -> int:
        """Subtract second integer from first.
        
        Args:
            a: First integer
            b: Second integer to subtract
            
        Returns:
            Difference between the two integers
        """
        return a - b

    def multiply(self, a: int, b: int) -> int:
        """Multiply two integers.
        
        Args:
            a: First integer
            b: Second integer
            
        Returns:
            Product of the two integers
        """
        return a * b