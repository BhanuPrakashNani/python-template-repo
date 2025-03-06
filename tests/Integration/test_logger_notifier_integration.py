"""Integration test for Logger and Notifier components."""

from pytest import CaptureFixture

from logger import Logger
from notifier import Notifier

def test_logger_notifier_integration(capsys: CaptureFixture[str]) -> None:
    """Test that Logger and Notifier work together correctly."""
    logger = Logger()
    notifier = Notifier()

    logger.log("Test log message")
    notifier.notify("Test notification message")

    captured = capsys.readouterr()
    assert "LOG: Test log message" in captured.out
    assert "NOTIFICATION: Test notification message" in captured.out
