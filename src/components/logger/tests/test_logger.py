from io import StringIO
import sys

import pytest
from logger import Logger

def test_log(capsys):
    logger = Logger()
    logger.log("Test message")
    captured = capsys.readouterr()
    assert captured.out == "LOG: Test message\n"

def test_multiple_logs(capsys):
    logger = Logger()
    logger.log("First message")
    logger.log("Second message")
    captured = capsys.readouterr()
    assert captured.out == "LOG: First message\nLOG: Second message\n"
