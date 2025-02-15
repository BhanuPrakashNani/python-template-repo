from src.notifier import Notifier
import unittest

def test_notify(capsys):
    notifier = Notifier()
    notifier.notify("Test message")
    captured = capsys.readouterr()
    assert captured.out == "NOTIFICATION: Test message\n"
