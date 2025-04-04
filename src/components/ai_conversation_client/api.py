"""AI Conversation Client interface module.

Defines the abstract interface for interacting with AI conversation services.
"""

from datetime import datetime


class AIConversationClient:
    """Interface for interacting with AI conversation services.

    This abstract class defines the standard interface that all AI conversation client
    implementations must follow.
    """

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize a new AI conversation client instance.

        Args:
            api_key: Optional API key for authentication with the service.
        """
        raise NotImplementedError()

    def send_message(
        self, session_id: str, message: str, attachments: list[str] | None = None
    ) -> dict[str, str | list[str] | datetime]:
        """Send a message to the AI service and get a response.

        Args:
            session_id: Unique identifier for the conversation session.
            message: The text message to send to the AI.
            attachments: Optional list of file paths or URLs to include.

        Returns:
            Dictionary containing:
                - response: The AI's text response
                - attachments: List of generated files (if any)
                - timestamp: When the response was generated
        """
        raise NotImplementedError()

    def get_chat_history(
        self, session_id: str, limit: int | None = None
    ) -> list[dict[str, str | datetime]]:
        """Retrieve conversation history for a session.

        Args:
            session_id: Unique identifier for the conversation session.
            limit: Maximum number of messages to retrieve.

        Returns:
            List of message dictionaries containing:
                - id: Message identifier
                - content: Message text
                - sender: 'user' or 'ai'
                - timestamp: When message was sent
        """
        raise NotImplementedError()

    def start_new_session(self, user_id: str, model: str | None = None) -> str:
        """Start a new conversation session.

        Args:
            user_id: Unique identifier for the user.
            model: Optional model identifier to use.

        Returns:
            New session identifier.
        """
        raise NotImplementedError()

    def end_session(self, session_id: str) -> bool:
        """End an active conversation session.

        Args:
            session_id: Session identifier to end.

        Returns:
            True if session was ended successfully, False otherwise.
        """
        raise NotImplementedError()

    def list_available_models(self) -> list[dict[str, str | list[str] | int]]:
        """Get available AI models with their capabilities.

        Returns:
            List of model dictionaries containing:
                - id: Model identifier
                - name: Human-readable name
                - capabilities: List of supported features
                - max_tokens: Maximum context length
        """
        raise NotImplementedError()

    def switch_model(self, session_id: str, model_id: str) -> bool:
        """Change the AI model for an active session.

        Args:
            session_id: Active session identifier.
            model_id: New model identifier to switch to.

        Returns:
            True if model was switched successfully, False otherwise.
        """
        raise NotImplementedError()

    def attach_file(
        self, session_id: str, file_path: str, description: str | None = None
    ) -> bool:
        """Attach a file to the conversation context.

        Args:
            session_id: Active session identifier.
            file_path: Path or URL to the file.
            description: Optional description of the file.

        Returns:
            True if file was attached successfully, False otherwise.
        """
        raise NotImplementedError()

    def get_usage_metrics(self, session_id: str) -> dict[str, int | float]:
        """Get usage statistics for a session.

        Args:
            session_id: Session identifier to check.

        Returns:
            Dictionary containing:
                - token_count: Total tokens used
                - api_calls: Number of API requests
                - cost_estimate: Estimated cost
        """
        raise NotImplementedError()
