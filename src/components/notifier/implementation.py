from .api import NotifierAPI

class Notifier:
    """Implementation of the Notifier component.
    
    This class provides notification functionality for important events.
    """
    
    def notify(self, message: str) -> None:
        """Send a notification with the given message.
        
        Args:
            message: The message to include in the notification
        """
        print(f"NOTIFICATION: {message}")