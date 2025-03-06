import pytest
from calculator import Calculator
from logger import Logger
from notifier import Notifier

def test_full_calculation_workflow(capsys):
    """Test the complete workflow from calculation to notification."""
    
    # Initialize components
    calc = Calculator()
    logger = Logger()
    notifier = Notifier()
    
    # Step 1: Perform calculations
    result1 = calc.multiply(4, 5)
    result2 = calc.add(result1, 10)
    
    # Step 2: Log the operations
    logger.log(f"Multiplication: 4 * 5 = {result1}")
    logger.log(f"Addition: {result1} + 10 = {result2}")
    
    # Step 3: Notify if result exceeds threshold
    threshold = 25
    if result2 > threshold:
        notifier.notify(f"Final result {result2} exceeds threshold {threshold}")
    
    # Verify the complete workflow
    captured = capsys.readouterr()
    expected_output = (
        "LOG: Multiplication: 4 * 5 = 20\n"
        "LOG: Addition: 20 + 10 = 30\n"
        "NOTIFICATION: Final result 30 exceeds threshold 25\n"
    )
    assert captured.out == expected_output
    assert result2 == 30
