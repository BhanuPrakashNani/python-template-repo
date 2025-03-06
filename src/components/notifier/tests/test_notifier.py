import pytest
from notifier import Notifier

def test_notify(capsys):
    notifier = Notifier()
    notifier.notify("Test alert")
    captured = capsys.readouterr()
    assert captured.out == "NOTIFICATION: Test alert\n"

def test_multiple_notifications(capsys):
    notifier = Notifier()
    notifier.notify("First alert")
    notifier.notify("Second alert")
    captured = capsys.readouterr()
    assert captured.out == "NOTIFICATION: First alert\nNOTIFICATION: Second alert\n"
