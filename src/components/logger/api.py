from dataclasses import dataclass
from typing import Protocol

class LoggerAPI(Protocol):
    def log(self, message: str) -> None:
        """Log a message.

        Args:
            message: The message to log
        """
        ...

@dataclass
class Logger:
    """Logger implementation that records operations."""
    
    def log(self, message: str) -> None:
        """Log a message with a LOG prefix."""
        print(f"LOG: {message}")
