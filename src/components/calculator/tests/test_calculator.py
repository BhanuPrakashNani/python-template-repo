"""Unit tests for the Calculator class."""

from typing import Any

from pytest import CaptureFixture

from ..calculator import Calculator


def test_add() -> None:
    """Test the add method."""
    calc = Calculator()
    assert calc.add(2, 3) == 5


def test_subtract() -> None:
    """Test the subtract method."""
    calc = Calculator()
    assert calc.subtract(5, 3) == 2


def test_multiply() -> None:
    """Test the multiply method."""
    calc = Calculator()
    assert calc.multiply(2, 3) == 6
