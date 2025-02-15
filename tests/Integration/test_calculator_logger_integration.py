from src.calculator import Calculator
from src.logger import Logger

def test_calculator_logger_integration(capsys):
    calc = Calculator()
    logger = Logger()

    result = calc.add(2, 3)
    logger.log(f"Result: {result}")

    captured = capsys.readouterr()
    assert captured.out == "LOG: Result: 5\n"