import pytest
from calculator import Calculator

def test_add():
    calc = Calculator()
    assert calc.add(1, 2) == 3
    assert calc.add(-1, 1) == 0
    assert calc.add(0, 0) == 0

def test_subtract():
    calc = Calculator()
    assert calc.subtract(3, 2) == 1
    assert calc.subtract(1, 1) == 0
    assert calc.subtract(0, 5) == -5

def test_multiply():
    calc = Calculator()
    assert calc.multiply(2, 3) == 6
    assert calc.multiply(-2, 3) == -6
    assert calc.multiply(0, 5) == 0
