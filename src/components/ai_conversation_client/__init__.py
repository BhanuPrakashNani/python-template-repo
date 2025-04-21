"""AI Conversation Client package.

This package provides a high-level interface for interacting with AI conversation
services like Cerebras. The package is designed around dependency injection and
follows proper abstraction principles.

Example usage:
    ```python
    from src.components.ai_conversation_client import get_client
    
    # Get a client instance (factory handles API key retrieval)
    client = get_client("cerebras")
    
    # Start a conversation
    session_id = client.start_new_session("user123")
    
    # Send a message
    response = client.send_message(session_id, "Hello, AI!")
    print(response["response"])
    ```
"""

from typing import Optional

from src.components.ai_conversation_client.api import AIConversationClient
from src.components.ai_conversation_client.cerebras_client import CerebrasClient
from src.components.ai_conversation_client.factory import AIClientFactory
from src.components.ai_conversation_client.mock_client import MockAIClient


# Register available clients (this happens when the package is imported)
AIClientFactory.register_client("cerebras", CerebrasClient)
AIClientFactory.register_client("mock", MockAIClient)


def get_client(client_name: str, api_key: Optional[str] = None, **kwargs) -> AIConversationClient:
    """Get an AI conversation client instance.
    
    This is the main factory function to get a client instance. It uses dependency
    injection to create the appropriate client based on the client_name.
    
    Args:
        client_name: Name of the client implementation to use.
        api_key: Optional API key. If not provided, will be read from environment variables.
        **kwargs: Additional arguments to pass to the client constructor.
        
    Returns:
        An instance of a class implementing the AIConversationClient interface.
        
    Raises:
        ValueError: If the requested client is not available.
    """
    return AIClientFactory.create_client(client_name, api_key=api_key, **kwargs)


__all__ = [
    "AIConversationClient",
    "CerebrasClient",
    "MockAIClient",
    "AIClientFactory",
    "get_client",
]
