"""Logger component implementation."""

class Logger:
    def log(self, message: str) -> None:
        """Log a message to the console.

        Args:
            message: The message to log.
        """
        print(f"LOG: {message}")
