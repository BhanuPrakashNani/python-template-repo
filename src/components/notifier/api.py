from typing import Protocol

class NotifierAPI(Protocol):
    """Protocol defining the Notifier component's API."""
    
    def notify(self, message: str) -> None:
        """Send a notification with the given message.
        
        Args:
            message: The message to include in the notification
        """
        ...