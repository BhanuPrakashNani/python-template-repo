from src.logger import Logger


def test_log(capsys):
    logger = Logger()
    logger.log("Test message")
    captured = capsys.readouterr()
    assert captured.out == "LOG: Test message\n"
