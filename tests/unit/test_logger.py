from src.logger import Logger
import unittest

def test_log(capsys):
    logger = Logger()
    logger.log("Test message")
    captured = capsys.readouterr()
    assert captured.out == "LOG: Test message\n"
