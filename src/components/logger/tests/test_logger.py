"""Unit tests for the Logger class."""

from pytest import CaptureFixture

from ..logger import Logger


def test_log(capsys: CaptureFixture[str]) -> None:
    """Test the log method captures correct output."""
    logger = Logger()
    logger.log("Test message")
    captured = capsys.readouterr()
    assert captured.out == "LOG: Test message\n"
