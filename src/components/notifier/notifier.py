"""Notifier component implementation."""

class Notifier:
    def notify(self, message: str) -> None:
        """Send a notification with the given message.

        Args:
            message: The notification message to send.
        """
        print(f"NOTIFICATION: {message}")
