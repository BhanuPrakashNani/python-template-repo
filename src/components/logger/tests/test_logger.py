"""Unit tests for the Logger class."""

from ..logger import Logger

def test_log(capsys):
    """Test the log method captures correct output."""
    logger = Logger()
    logger.log("Test message")
    captured = capsys.readouterr()
    assert captured.out == "LOG: Test message\n"
