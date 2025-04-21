"""AI Conversation Client factory module.

This module provides a factory for creating instances of AI conversation clients.
It implements dependency injection for client implementations, making it easier to swap
implementations or configure clients as needed.
"""

from typing import Dict, Optional, Type, Union, Any

from src.components.ai_conversation_client.api import AIConversationClient


class AIClientFactory:
    """Factory for creating AI conversation client instances.

    This factory manages the creation and configuration of AI conversation clients,
    supporting dependency injection and configuration of different client
    implementations.
    """

    _client_registry: Dict[str, Type[AIConversationClient]] = {}

    @classmethod
    def register_client(
        cls, client_name: str, client_class: Type[AIConversationClient]
    ) -> None:
        """Register a client implementation with the factory.

        Args:
            client_name: Name to register the client under.
            client_class: Client class implementing the AIConversationClient interface.
        """
        cls._client_registry[client_name] = client_class

    @classmethod
    def create_client(
        cls, client_name: str, api_key: str | None = None, **kwargs: Dict[str, Any]
    ) -> AIConversationClient:
        """Create a new client instance.

        Args:
            client_name: Name of the registered client implementation to create.
            api_key: Optional API key to pass to the client.
            **kwargs: Additional arguments to pass to the client constructor.

        Returns:
            A configured AIConversationClient instance.

        Raises:
            ValueError: If the requested client name is not registered.
        """
        if client_name not in cls._client_registry:
            available_clients = ", ".join(cls._client_registry.keys())
            raise ValueError(
                f"Client '{client_name}' not found. "
                f"Available clients: {available_clients}"
            )

        client_class = cls._client_registry[client_name]
        return client_class(api_key=api_key, **kwargs)

    @classmethod
    def list_available_clients(cls) -> Dict[str, Type[AIConversationClient]]:
        """Get all registered client implementations.

        Returns:
            Dictionary mapping client names to their implementing classes.
        """
        return cls._client_registry.copy() 