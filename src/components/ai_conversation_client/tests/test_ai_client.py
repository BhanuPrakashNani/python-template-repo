"""Tests for the AI Conversation Client abstract interface using the mock client."""

from datetime import datetime

import pytest

from src.components.ai_conversation_client.api import AIConversationClient
from src.components.ai_conversation_client.factory import AIClientFactory
from src.components.ai_conversation_client.mock_client import MockAIClient


class TestAIClientInterface:
    """Test suite for the AIConversationClient interface using MockAIClient."""

    @pytest.fixture
    def client(self) -> AIConversationClient:
        """Provide a mock client instance for testing.

        Returns:
            A MockAIClient instance implementing the AIConversationClient interface.
        """
        return AIClientFactory.create_client("mock")

    def test_factory_registration(self) -> None:
        """Test that clients are properly registered with the factory."""
        # Get available clients
        clients = AIClientFactory.list_available_clients()

        # Check that the mock client is registered
        assert "mock" in clients
        assert clients["mock"] == MockAIClient

    def test_factory_create_client(self) -> None:
        """Test creation of a client instance through the factory."""
        # Create a client
        client = AIClientFactory.create_client("mock")

        # Check that it's the right type
        assert isinstance(client, MockAIClient)
        assert isinstance(client, AIConversationClient)

    def test_factory_unknown_client(self) -> None:
        """Test that the factory raises an error for unknown clients."""
        with pytest.raises(ValueError) as excinfo:
            AIClientFactory.create_client("nonexistent")
        assert "Client 'nonexistent' not found" in str(excinfo.value)

    def test_start_new_session(self, client: AIConversationClient) -> None:
        """Test starting a new session."""
        user_id = "test_user"
        session_id = client.start_new_session(user_id)

        # Check that the session ID is a string (likely a UUID)
        assert isinstance(session_id, str)
        assert len(session_id) > 0

    def test_start_new_session_with_model(self, client: AIConversationClient) -> None:
        """Test starting a new session with a specific model."""
        user_id = "test_user"
        model_id = "mock-gpt-3"  # This model should exist in the mock client
        session_id = client.start_new_session(user_id, model=model_id)

        # We can't directly check the model as that's implementation-specific,
        # but we can make sure the session was created successfully
        assert isinstance(session_id, str)

    def test_start_new_session_invalid_model(
        self, client: AIConversationClient
    ) -> None:
        """Test that starting a session with an invalid model raises an error."""
        with pytest.raises(ValueError) as excinfo:
            client.start_new_session("test_user", model="nonexistent-model")
        assert "not available" in str(excinfo.value)

    def test_send_message(self, client: AIConversationClient) -> None:
        """Test sending a message and getting a response."""
        # Create a session
        user_id = "test_user"
        session_id = client.start_new_session(user_id)

        # Send a message
        message = "Hello, AI!"
        response = client.send_message(session_id, message)

        # Check the response format
        assert isinstance(response, dict)
        assert "response" in response
        assert isinstance(response["response"], str)
        assert "timestamp" in response
        assert isinstance(response["timestamp"], datetime)
        assert "attachments" in response
        assert isinstance(response["attachments"], list)

    def test_send_message_nonexistent_session(
        self, client: AIConversationClient
    ) -> None:
        """Test that sending a message to a nonexistent session raises an error."""
        with pytest.raises(ValueError) as excinfo:
            client.send_message("nonexistent-session", "Hello")
        assert "does not exist" in str(excinfo.value)

    def test_get_chat_history(self, client: AIConversationClient) -> None:
        """Test retrieving chat history after sending messages."""
        # Create a session
        user_id = "test_user"
        session_id = client.start_new_session(user_id)

        # Send a message
        client.send_message(session_id, "Hello")

        # Get chat history
        history = client.get_chat_history(session_id)

        # Check history format
        assert isinstance(history, list)
        assert len(history) == 2  # User message and AI response

        # Check first message (user)
        assert history[0]["content"] == "Hello"
        assert history[0]["sender"] == "user"
        assert isinstance(history[0]["id"], str)
        assert isinstance(history[0]["timestamp"], datetime)

        # Check second message (AI)
        assert isinstance(history[1]["content"], str)
        assert history[1]["sender"] == "assistant"
        assert isinstance(history[1]["id"], str)
        assert isinstance(history[1]["timestamp"], datetime)

    def test_get_chat_history_with_limit(self, client: AIConversationClient) -> None:
        """Test retrieving chat history with a limit."""
        # Create a session
        user_id = "test_user"
        session_id = client.start_new_session(user_id)

        # Send multiple messages
        client.send_message(session_id, "Message 1")
        client.send_message(session_id, "Message 2")

        # Should now have 4 messages (2 user, 2 AI)
        # Get limited history
        history = client.get_chat_history(session_id, limit=2)

        # Check we only got the last 2 messages
        assert len(history) == 2

    def test_end_session(self, client: AIConversationClient) -> None:
        """Test ending a session."""
        # Create a session
        user_id = "test_user"
        session_id = client.start_new_session(user_id)

        # End the session
        result = client.end_session(session_id)
        assert result is True

    def test_end_nonexistent_session(self, client: AIConversationClient) -> None:
        """Test ending a nonexistent session."""
        result = client.end_session("nonexistent-session")
        assert result is False

    def test_list_available_models(self, client: AIConversationClient) -> None:
        """Test listing available models."""
        models = client.list_available_models()

        # Check format
        assert isinstance(models, list)
        assert len(models) > 0

        # Check model structure
        for model in models:
            assert isinstance(model, dict)
            assert "id" in model
            assert "name" in model
            assert "capabilities" in model
            assert isinstance(model["capabilities"], list)
            assert "max_tokens" in model
            assert isinstance(model["max_tokens"], int)

    def test_switch_model(self, client: AIConversationClient) -> None:
        """Test switching models for a session."""
        # Create a session
        user_id = "test_user"
        session_id = client.start_new_session(user_id)

        # Switch to a different model
        result = client.switch_model(session_id, "mock-gpt-3")
        assert result is True

    def test_switch_model_invalid(self, client: AIConversationClient) -> None:
        """Test switching to an invalid model."""
        # Create a session
        user_id = "test_user"
        session_id = client.start_new_session(user_id)

        # Switch to nonexistent model
        with pytest.raises(ValueError) as excinfo:
            client.switch_model(session_id, "nonexistent-model")
        assert "not available" in str(excinfo.value)

    def test_get_usage_metrics(self, client: AIConversationClient) -> None:
        """Test retrieving usage metrics."""
        # Create a session
        user_id = "test_user"
        session_id = client.start_new_session(user_id)

        # Send a message to generate metrics
        client.send_message(session_id, "Hello")

        # Get metrics
        metrics = client.get_usage_metrics(session_id)

        # Check metrics format
        assert isinstance(metrics, dict)
        assert "token_count" in metrics
        assert isinstance(metrics["token_count"], int | float)
        assert "api_calls" in metrics
        assert isinstance(metrics["api_calls"], int | float)
        assert "cost_estimate" in metrics
        assert isinstance(metrics["cost_estimate"], int | float)

    def test_summarize_conversation(self, client: AIConversationClient) -> None:
        """Test summarizing a conversation."""
        # Create a session
        user_id = "test_user"
        session_id = client.start_new_session(user_id)

        # Send messages
        client.send_message(session_id, "Hello, how are you?")
        client.send_message(session_id, "Tell me about Python.")

        # Summarize
        summary = client.summarize_conversation(session_id)

        # Check format
        assert isinstance(summary, str)
        assert len(summary) > 0

    def test_export_chat_history_json(self, client: AIConversationClient) -> None:
        """Test exporting chat history in JSON format."""
        # Create a session
        user_id = "test_user"
        session_id = client.start_new_session(user_id)

        # Send a message
        client.send_message(session_id, "Hello")

        # Export as JSON
        export = client.export_chat_history(session_id, format="json")

        # Check format
        assert isinstance(export, str)
        assert "{" in export  # Basic JSON structure check
        assert "messages" in export
        assert "Hello" in export

    def test_export_chat_history_txt(self, client: AIConversationClient) -> None:
        """Test exporting chat history in text format."""
        # Create a session
        user_id = "test_user"
        session_id = client.start_new_session(user_id)

        # Send a message
        client.send_message(session_id, "Hello")

        # Export as text
        export = client.export_chat_history(session_id, format="txt")

        # Check format
        assert isinstance(export, str)
        assert "User: Hello" in export
