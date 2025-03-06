from typing import Protocol

class LoggerAPI(Protocol):
    """Protocol defining the Logger component's API."""
    
    def log(self, message: str) -> None:
        """Log a message.
        
        Args:
            message: The message to log
        """
        ...