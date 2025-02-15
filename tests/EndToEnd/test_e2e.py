from src.calculator import Calculator
from src.logger import Logger
from src.notifier import Notifier
import unittest

def test_e2e_workflow(capsys):
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