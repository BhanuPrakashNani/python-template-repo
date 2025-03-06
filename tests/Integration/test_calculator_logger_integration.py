"""Integration test for Calculator and Logger components."""

from pytest import CaptureFixture

from calculator import Calculator
from logger import Logger


def test_calculator_logger_integration(capsys: CaptureFixture[str]) -> None:
    """Test that Calculator operations are correctly logged."""
    calc = Calculator()
    logger = Logger()

    result = calc.add(2, 3)
    logger.log(f"Result: {result}")

    captured = capsys.readouterr()
    assert captured.out == "LOG: Result: 5\n"
