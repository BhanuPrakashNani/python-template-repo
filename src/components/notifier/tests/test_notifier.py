"""Unit tests for the Notifier class."""

from pytest import CaptureFixture

from ..notifier import Notifier

def test_notify(capsys: CaptureFixture[str]) -> None:
    """Test the notify method captures correct output."""
    notifier = Notifier()
    notifier.notify("Test message")
    captured = capsys.readouterr()
    assert captured.out == "NOTIFICATION: Test message\n"
