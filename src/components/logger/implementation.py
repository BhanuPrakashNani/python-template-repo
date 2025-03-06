from .api import LoggerAPI

class Logger:
    """Implementation of the Logger component.
    
    This class provides logging functionality for messages.
    """
    
    def log(self, message: str) -> None:
        """Log a message.
        
        Args:
            message: The message to log
        """
        print(f"LOG: {message}")