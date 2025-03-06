from dataclasses import dataclass
from typing import Protocol

class NotifierAPI(Protocol):
    def notify(self, message: str) -> None:
        """Send a notification.

        Args:
            message: The message to send
        """
        ...

@dataclass
class Notifier:
    """Notifier implementation that sends alerts."""
    
    def notify(self, message: str) -> None:
        """Send a notification with a NOTIFICATION prefix."""
        print(f"NOTIFICATION: {message}")
