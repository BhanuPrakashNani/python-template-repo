"""Unit tests for the Calculator class."""

from ..calculator import Calculator

def test_add():
    """Test the add method."""
    calc = Calculator()
    assert calc.add(2, 3) == 5

def test_subtract():
    """Test the subtract method."""
    calc = Calculator()
    assert calc.subtract(5, 3) == 2

def test_multiply():
    """Test the multiply method."""
    calc = Calculator()
    assert calc.multiply(2, 3) == 6
