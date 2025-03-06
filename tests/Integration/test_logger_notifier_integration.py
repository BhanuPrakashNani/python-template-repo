from src.components.logger.logger import Logger
from src.components.notifier.notifier import Notifier


def test_logger_notifier_integration(capsys):
    logger = Logger()
    notifier = Notifier()

    logger.log("Test log message")
    notifier.notify("Test notification message")

    captured = capsys.readouterr()
    assert "LOG: Test log message" in captured.out
    assert "NOTIFICATION: Test notification message" in captured.out
