"""AI Conversation Client interface module.

Defines the abstract interface for interacting with AI conversation services.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Protocol


class AIConversationClientInterface(ABC):
    """Abstract interface for interacting with AI conversation services.

    This interface defines the standard contract that all AI conversation client
    implementations must follow.
    """

    @abstractmethod
    def __init__(self, api_key: str | None = None) -> None:
        """Initialize a new AI conversation client instance.

        Args:
            api_key: Optional API key for authentication with the service.
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
        """
        pass

    @abstractmethod
    def start_new_session(self, user_id: str, model: str | None = None) -> str:
        """Start a new conversation session.

        Args:
            user_id: Unique identifier for the user.
            model: Optional model identifier to use.

        Returns:
            New session identifier.
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
    def list_available_models(self) -> list[dict[str, str | list[str] | int]]:
        """Get available AI models with their capabilities.

        Returns:
            List of model dictionaries containing:
                - id: Model identifier
                - name: Human-readable name
                - capabilities: List of supported features
                - max_tokens: Maximum context length
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
        """
        pass

    @abstractmethod
    def summarize_conversation(self, session_id: str) -> str:
        """Generate a summary of the entire conversation.

        Args:
            session_id: Session identifier for conversation to summarize.

        Returns:
            Summary of the conversation as a string.
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
        """
        pass


class APIClientProtocol(Protocol):
    """Protocol for API client to be used with AIConversationClientInterface."""

    def send_message(
        self, session_id: str, message: str, attachments: list[str] | None = None
    ) -> dict[str, str | list[str] | datetime]:
        """Send a message to the AI service and receive a response.

        Args:
            self: Instance of the AIConversationClientInterface.
            session_id: Unique identifier of the session.
            message: User's message to the AI.
            attachments: Optional list of file paths or URLs to include with the message

        Returns:
            A dictionary containing:
                - 'response': The AI's generated reply.
                - 'attachments': List of any files generated or returned.
                - 'timestamp': Time the response was generated.
        """
        ...

    def get_chat_history(
        self, session_id: str, limit: int | None = None
    ) -> list[dict[str, str | datetime]]:
        """Retrieve the message history for a session.

        Args:
            self: Instance of the AIConversationClientInterface.
            session_id: The ID of the session to retrieve history for.
            limit: Optional maximum number of recent messages to retrieve.

        Returns:
            A list of dictionaries containing:
                - 'id': Message ID.
                - 'content': Message text.
                - 'sender': Either 'user' or 'ai'.
                - 'timestamp': When the message was sent.
        """
        ...

    def start_new_session(self, user_id: str, model: str | None = None) -> str:
        """Start a new AI conversation session for a user.

        Args:
            self: Instance of the AIConversationClientInterface.
            user_id: Unique identifier of the user.
            model: Optional model ID to use for the session.

        Returns:
            A unique session ID for the newly created conversation.
        """
        ...

    def end_session(self, session_id: str) -> bool:
        """End an active conversation session.

        Args:
            self: Instance of the AIConversationClientInterface.
            session_id: ID of the session to terminate.

        Returns:
            True if the session was ended successfully, False otherwise.
        """
        ...

    def list_available_models(self) -> list[dict[str, str | list[str] | int]]:
        """Get a list of available AI models and their capabilities.

        Args:
            self: Instance of the AIConversationClientInterface.

        Returns:
            A list of dictionaries describing available models:
                - 'id': Model identifier.
                - 'name': Human-readable name of the model.
                - 'capabilities': List of supported features (e.g., chat, code).
                - 'max_tokens': Maximum token length for input context.
        """
        ...

    def switch_model(self, session_id: str, model_id: str) -> bool:
        """Switch the AI model used for an ongoing session.

        Args:
            self: Instance of the AIConversationClientInterface.
            session_id: ID of the session to update.
            model_id: ID of the new model to assign to the session.

        Returns:
            True if the model was successfully switched, False otherwise.
        """
        ...

    def attach_file(
        self, session_id: str, file_path: str, description: str | None = None
    ) -> bool:
        """Attach a file to the session's conversation context.

        Args:
            self: Instance of the AIConversationClientInterface.
            session_id: The session to which the file is being attached.
            file_path: Path to the file or URL.
            description: Optional description of the file.

        Returns:
            True if the file was successfully attached, False otherwise.
        """
        ...

    def get_usage_metrics(self, session_id: str) -> dict[str, int | float]:
        """Get usage statistics for a session.

        Args:
            self: Instance of the AIConversationClientInterface.
            session_id: ID of the session to analyze.

        Returns:
            A dictionary containing:
                - 'token_count': Estimated number of tokens used.
                - 'api_calls': Number of messages sent/received.
                - 'cost_estimate': Approximate API cost incurred.
        """
        ...

    def summarize_conversation(self, session_id: str) -> str:
        """Generate a summary of the conversation in the session.

        Args:
            self: Instance of the AIConversationClientInterface.
            session_id: ID of the session to summarize.

        Returns:
            A string containing the AI-generated or algorithmic summary of the chat.
        """
        ...

    def export_chat_history(self, session_id: str, format: str = "json") -> str:
        """Export the full chat history for a session to a file.

        Args:
            self: Instance of the AIConversationClientInterface.
            session_id: The session whose history is being exported.
            format: Desired export format, such as 'json' or 'txt'.

        Returns:
            The path to the exported file.

        Raises:
            ValueError: If the provided format is unsupported.
        """
        ...
