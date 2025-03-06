"""End-to-end tests for the complete workflow."""

from pytest import CaptureFixture

from calculator import Calculator
from logger import Logger
from notifier import Notifier

def test_e2e_workflow(capsys: CaptureFixture[str]) -> None:
    """Test the complete workflow of Calculator, Logger, and Notifier."""
    calc = Calculator()
    logger = Logger()
    notifier = Notifier()

    # Perform a calculation
    result = calc.multiply(4, 5)

    # Log the result
    logger.log(f"Multiplication result: {result}")

    # Notify if the result exceeds a threshold
    threshold = 15
    if result > threshold:
        notifier.notify(f"Result {result} exceeds threshold {threshold}")

    # Capture output
    captured = capsys.readouterr()

    # Verify logs and notifications
    assert "LOG: Multiplication result: 20" in captured.out
    assert "NOTIFICATION: Result 20 exceeds threshold 15" in captured.out
