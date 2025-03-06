"""Unit tests for the Notifier class."""

from ..notifier import Notifier

def test_notify(capsys):
    """Test the notify method captures correct output."""
    notifier = Notifier()
    notifier.notify("Test message")
    captured = capsys.readouterr()
    assert captured.out == "NOTIFICATION: Test message\n"
