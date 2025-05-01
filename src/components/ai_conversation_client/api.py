"""AI Conversation Client interface module.

Defines the abstract interface for interacting with AI conversation services.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class AIConversationClient(ABC):
    """Interface for interacting with AI conversation services.

    This abstract base class defines the standard interface that all AI conversation
    client implementations must follow. Concrete subclasses must implement all abstract
    methods.
    """

    @abstractmethod
    def __init__(self, api_key: str | None = None) -> None:
        """Initialize a new AI conversation client instance.

        Args:
            api_key: Optional API key for authentication with the service.
                     If not provided, the client should look for credentials
                     in environment variables.
        """
        pass

    @abstractmethod
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

        Raises:
            ValueError: If the session_id does not exist.
            RuntimeError: If the API request fails.
        """
        pass

    @abstractmethod
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

        Raises:
            ValueError: If the session_id does not exist.
        """
        pass

    @abstractmethod
    def start_new_session(self, user_id: str, model: str | None = None) -> str:
        """Start a new conversation session.

        Args:
            user_id: Unique identifier for the user.
            model: Optional model identifier to use. Implementation may use a default
                  if none is specified.

        Returns:
            New session identifier.

        Raises:
            ValueError: If the specified model is not available.
        """
        pass

    @abstractmethod
    def end_session(self, session_id: str) -> bool:
        """End an active conversation session.

        Args:
            session_id: Session identifier to end.

        Returns:
            True if session was ended successfully, False otherwise.
        """
        pass

    @abstractmethod
    def list_available_models(self) -> list[dict[str, str | list[str] | int | bool]]:
        """Get available AI models with their capabilities.

        Returns:
            List of model dictionaries containing:
                - id: Model identifier
                - name: Human-readable name
                - capabilities: List of supported features
                - max_tokens: Maximum context length
                - optional additional model-specific properties
        """
        pass

    @abstractmethod
    def switch_model(self, session_id: str, model_id: str) -> bool:
        """Change the AI model for an active session.

        Args:
            session_id: Active session identifier.
            model_id: New model identifier to switch to.

        Returns:
            True if model was switched successfully, False otherwise.

        Raises:
            ValueError: If the session_id does not exist or the model_id is invalid.
        """
        pass

    @abstractmethod
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

        Raises:
            ValueError: If the session_id does not exist.
            FileNotFoundError: If the file cannot be found or accessed.
        """
        pass

    @abstractmethod
    def get_usage_metrics(self, session_id: str) -> dict[str, int | float]:
        """Get usage statistics for a session.

        Args:
            session_id: Session identifier to check.

        Returns:
            Dictionary containing:
                - token_count: Total tokens used
                - api_calls: Number of API requests
                - cost_estimate: Estimated cost

        Raises:
            ValueError: If the session_id does not exist.
        """
        pass

    @abstractmethod
    def summarize_conversation(self, session_id: str) -> str:
        """Generate summary of the entire conversation.

        Args:
            session_id: Session identifier for conversation to summarize.

        Returns:
            Summary of the conversation as a string.

        Raises:
            ValueError: If the session_id does not exist.
            RuntimeError: If the summarization fails.
        """
        pass

    @abstractmethod
    def export_chat_history(self, session_id: str, format: str = "json") -> str:
        """Export chat history to a specified format.

        Args:
            session_id: Session identifier for the conversation.
            format: Format to export the chat history (e.g., 'json', 'txt').

        Returns:
            Path to the exported file or string representation of the chat history.

        Raises:
            ValueError: If the session_id does not exist or the format is unsupported.
        """
        pass
