"""Tests for the Cerebras implementation of AIConversationClient."""

import json
import os
import uuid
from datetime import datetime
from typing import Any, Tuple
from unittest.mock import MagicMock, Mock, patch

import pytest
import requests
from requests.exceptions import ConnectionError, Timeout

from src.components.ai_conversation_client.cerebras_client import CerebrasClient


class TestCerebrasClient:
    """Test suite for CerebrasClient implementation."""

    @pytest.fixture
    def mock_api_key(self) -> str:
        """Provide a mock API key for testing.

        Returns:
            A dummy API key string.
        """
        return "test_api_key_12345"

    @pytest.fixture
    def cerebras_client(self, mock_api_key: str) -> CerebrasClient:
        """Create a CerebrasClient instance for testing.

        Args:
            mock_api_key: The mock API key to use.

        Returns:
            A CerebrasClient instance.
        """
        with patch.dict(os.environ, {"CEREBRAS_API_KEY": mock_api_key}):
            client = CerebrasClient()
        return client

    def test_init_with_api_key(self, mock_api_key: str) -> None:
        """Test initialization with API key provided as a parameter."""
        client = CerebrasClient(api_key=mock_api_key)
        assert client.api_key == mock_api_key
        assert client._headers["Authorization"] == f"Bearer {mock_api_key}"

    def test_init_with_env_var(self) -> None:
        """Test initialization with API key from environment variable."""
        mock_api_key = "env_var_api_key"
        with patch.dict(os.environ, {"CEREBRAS_API_KEY": mock_api_key}):
            client = CerebrasClient()
            assert client.api_key == mock_api_key
            assert client._headers["Authorization"] == f"Bearer {mock_api_key}"

    def test_init_without_api_key(self) -> None:
        """Test initialization without an API key raises an error."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError) as excinfo:
                CerebrasClient()
            assert "API key must be provided" in str(excinfo.value)

    def test_list_available_models(self, cerebras_client: CerebrasClient) -> None:
        """Test list_available_models returns expected model list."""
        models = cerebras_client.list_available_models()
        assert isinstance(models, list)
        assert len(models) > 0
        assert all(isinstance(model, dict) for model in models)
        assert all("id" in model and "name" in model for model in models)

        # Verify the models match expected values from the latest documentation
        model_ids = [model["id"] for model in models]
        assert "llama-4-scout-17b-16e-instruct" in model_ids
        assert "llama3.1-8b" in model_ids
        assert "llama-3.3-70b" in model_ids

    def test_start_new_session(self, cerebras_client: CerebrasClient) -> None:
        """Test start_new_session creates a new session with expected properties."""
        user_id = "test_user_1"
        session_id = cerebras_client.start_new_session(user_id)

        assert isinstance(session_id, str)
        assert session_id in cerebras_client._sessions

        session = cerebras_client._sessions[session_id]
        assert session["user_id"] == user_id
        assert session["model"] == "llama-4-scout-17b-16e-instruct"  # Default model
        assert isinstance(session["history"], list)
        assert session["active"] is True

    def test_start_new_session_with_model(
        self, cerebras_client: CerebrasClient
    ) -> None:
        """Test start_new_session with a specific model."""
        user_id = "test_user_2"
        model_id = "llama3.1-8b"
        session_id = cerebras_client.start_new_session(user_id, model=model_id)

        session = cerebras_client._sessions[session_id]
        assert session["model"] == model_id

    def test_start_new_session_invalid_model(
        self, cerebras_client: CerebrasClient
    ) -> None:
        """Test start_new_session with an invalid model raises an error."""
        with pytest.raises(ValueError) as excinfo:
            cerebras_client.start_new_session("test_user", model="nonexistent-model")
        assert "not available" in str(excinfo.value)
        assert "nonexistent-model" in str(excinfo.value)

    def test_end_session(self, cerebras_client: CerebrasClient) -> None:
        """Test end_session marks a session as inactive."""
        user_id = "test_user_3"
        session_id = cerebras_client.start_new_session(user_id)

        result = cerebras_client.end_session(session_id)
        assert result is True
        assert cerebras_client._sessions[session_id]["active"] is False

    def test_end_nonexistent_session(self, cerebras_client: CerebrasClient) -> None:
        """Test end_session returns False for a nonexistent session."""
        nonexistent_id = "nonexistent-session-id"
        result = cerebras_client.end_session(nonexistent_id)
        assert result is False

    def test_send_message(self, cerebras_client: CerebrasClient) -> None:
        """Test send_message with a mocked API response."""
        # Create a session
        user_id = "test_user_4"
        session_id = cerebras_client.start_new_session(user_id)

        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {"message": {"content": "This is a test response from the AI."}}
            ],
            "usage": {"total_tokens": 45},
        }

        # Patch the requests.post method
        with patch("requests.post", return_value=mock_response):
            response = cerebras_client.send_message(session_id, "Test message")

        # Check the response
        assert isinstance(response, dict)
        assert "response" in response
        assert response["response"] == "This is a test response from the AI."
        assert "timestamp" in response
        assert isinstance(response["timestamp"], datetime)

        # Check that the message was added to the history
        history = cerebras_client.get_chat_history(session_id)
        assert len(history) == 3  # System message, user message, and AI response
        
        # Find the messages by sender
        system_messages = [msg for msg in history if msg["sender"] == "system"]
        user_messages = [msg for msg in history if msg["sender"] == "user"]
        ai_messages = [msg for msg in history if msg["sender"] == "assistant"]
        
        assert len(system_messages) == 1
        assert len(user_messages) == 1
        assert len(ai_messages) == 1
        
        assert user_messages[0]["content"] == "Test message"
        assert ai_messages[0]["content"] == "This is a test response from the AI."

        # Check that usage metrics were updated
        metrics = cerebras_client.get_usage_metrics(session_id)
        assert metrics["token_count"] == 45
        assert metrics["api_calls"] == 1

    def test_send_message_api_error(self, cerebras_client: CerebrasClient) -> None:
        """Test send_message handles API errors properly."""
        # Create a session
        user_id = "test_user_5"
        session_id = cerebras_client.start_new_session(user_id)

        # Patch requests.post to raise an exception
        with patch("requests.post", side_effect=requests.RequestException("API Error")):
            with pytest.raises(RuntimeError) as excinfo:
                cerebras_client.send_message(session_id, "Test message")

        assert "Failed to send message to Cerebras API" in str(excinfo.value)

    def test_get_chat_history(self, cerebras_client: CerebrasClient) -> None:
        """Test get_chat_history returns the expected chat history."""
        # Create a session and add some messages
        user_id = "test_user_6"
        session_id = cerebras_client.start_new_session(user_id)

        # Manually add messages to the history
        cerebras_client._sessions[session_id]["history"] = [
            {
                "id": str(uuid.uuid4()),
                "content": "Hello, AI!",
                "sender": "user",
                "timestamp": datetime.now(),
            },
            {
                "id": str(uuid.uuid4()),
                "content": "Hello, user! How can I help you?",
                "sender": "assistant",
                "timestamp": datetime.now(),
            },
            {
                "id": str(uuid.uuid4()),
                "content": "Tell me about Cerebras.",
                "sender": "user",
                "timestamp": datetime.now(),
            },
            {
                "id": str(uuid.uuid4()),
                "content": "Cerebras is an AI company...",
                "sender": "assistant",
                "timestamp": datetime.now(),
            },
        ]

        # Get the full history
        history = cerebras_client.get_chat_history(session_id)
        assert len(history) == 4

        # Get limited history
        limited_history = cerebras_client.get_chat_history(session_id, limit=2)
        assert len(limited_history) == 2
        assert limited_history[0]["content"] == "Tell me about Cerebras."
        assert limited_history[1]["content"] == "Cerebras is an AI company..."

    def test_get_chat_history_nonexistent_session(
        self, cerebras_client: CerebrasClient
    ) -> None:
        """Test get_chat_history raises an error for a nonexistent session."""
        with pytest.raises(ValueError) as excinfo:
            cerebras_client.get_chat_history("nonexistent-session")
        assert "Session nonexistent-session does not exist" in str(excinfo.value)

    def test_switch_model(self, cerebras_client: CerebrasClient) -> None:
        """Test switch_model changes the model for a session."""
        # Create a session
        user_id = "test_user_7"
        session_id = cerebras_client.start_new_session(user_id)

        # Switch to a different model
        result = cerebras_client.switch_model(session_id, "llama3.1-8b")
        assert result is True
        assert cerebras_client._sessions[session_id]["model"] == "llama3.1-8b"

    def test_switch_model_invalid(self, cerebras_client: CerebrasClient) -> None:
        """Test switch_model with an invalid model raises an error."""
        # Create a session
        user_id = "test_user_8"
        session_id = cerebras_client.start_new_session(user_id)

        # Try to switch to an invalid model
        with pytest.raises(ValueError) as excinfo:
            cerebras_client.switch_model(session_id, "nonexistent-model")
        assert "Model nonexistent-model is not available" in str(excinfo.value)

    def test_summarize_conversation(self, cerebras_client: CerebrasClient) -> None:
        """Test summarize_conversation with a mocked API response."""
        # Create a session and add some messages
        user_id = "test_user_9"
        session_id = cerebras_client.start_new_session(user_id)

        # Manually add messages to the history
        cerebras_client._sessions[session_id]["history"] = [
            {
                "id": "test-msg-1",
                "content": "Tell me about AI.",
                "sender": "user",
                "timestamp": datetime.now(),
            },
            {
                "id": "test-msg-2",
                "content": "AI stands for Artificial Intelligence...",
                "sender": "assistant",
                "timestamp": datetime.now(),
            },
        ]

        # Mock the API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {"message": {"content": "This conversation was about AI basics."}}
            ],
            "usage": {"total_tokens": 30},
        }

        # Patch the requests.post method and check correct data is sent
        with patch("requests.post", return_value=mock_response) as mock_post:
            summary = cerebras_client.summarize_conversation(session_id)

            # Verify the API call
            mock_post.assert_called_once()

            # Check that summary content is from the mocked response
            assert summary == "This conversation was about AI basics."

            # Check that the request was made with correct parameters
            _, kwargs = mock_post.call_args
            assert "json" in kwargs

            # Verify the messages format
            messages = kwargs["json"]["messages"]
            assert len(messages) == 2
            assert messages[0]["role"] == "system"
            assert "provide a concise summary" in messages[0]["content"].lower()
            assert messages[1]["role"] == "user"
            assert "user: tell me about ai" in messages[1]["content"].lower()
            content = messages[1]["content"].lower()
            assert "ai: ai stands for artificial intelligence" in content

    def test_export_chat_history(self, cerebras_client: CerebrasClient) -> None:
        """Test export_chat_history returns the expected JSON string."""
        # Create a session and add some messages
        user_id = "test_user_10"
        session_id = cerebras_client.start_new_session(user_id)

        # Manually add a message to the history
        msg_time = datetime.now()
        cerebras_client._sessions[session_id]["history"] = [
            {
                "id": "test-msg-id",
                "content": "Test message",
                "sender": "user",
                "timestamp": msg_time,
            }
        ]

        # Export the history to JSON
        json_str = cerebras_client.export_chat_history(session_id)

        # Verify it's valid JSON with the expected content
        assert "session_id" in json_str
        assert session_id in json_str
        assert user_id in json_str
        assert "Test message" in json_str
        assert "test-msg-id" in json_str

# Add new tests for error handling scenarios
class TestErrorHandling:
    """Test suite for error handling in CerebrasClient."""

    @pytest.fixture
    def cerebras_client(self) -> Tuple[CerebrasClient, str]:
        """Create a CerebrasClient with mocked API key."""
        with patch.dict(os.environ, {"CEREBRAS_API_KEY": "test-key"}):
            client = CerebrasClient()
            
            # Create a test session
            session_id = "test-session-id"
            client._sessions[session_id] = {
                "id": session_id,
                "user_id": "test-user",
                "model": "test-model",
                "active": True,
                "created_at": datetime.now(),
                "history": [],
                "metrics": {"token_count": 0, "api_calls": 0, "cost_estimate": 0.0},
            }
            return client, session_id
    
    def test_send_message_empty_message(self, cerebras_client: Tuple[CerebrasClient, str]) -> None:
        """Test error handling when sending an empty message."""
        client, session_id = cerebras_client
        
        with pytest.raises(ValueError) as e:
            client.send_message(session_id, "")
        
        assert "Message cannot be empty" in str(e.value)
        
        with pytest.raises(ValueError) as e:
            client.send_message(session_id, "   ")
        
        assert "Message cannot be empty" in str(e.value)
    
    def test_send_message_empty_session_id(self, cerebras_client: Tuple[CerebrasClient, str]) -> None:
        """Test error handling when sending a message with an empty session ID."""
        client, _ = cerebras_client
        
        with pytest.raises(ValueError) as e:
            client.send_message("", "Test message")
        
        assert "Session ID cannot be empty" in str(e.value)
    
    def test_send_message_inactive_session(self, cerebras_client: Tuple[CerebrasClient, str]) -> None:
        """Test error handling when sending a message to an inactive session."""
        client, session_id = cerebras_client
        
        # Mark the session as inactive
        client._sessions[session_id]["active"] = False
        
        with pytest.raises(ValueError) as e:
            client.send_message(session_id, "Test message")
        
        assert "no longer active" in str(e.value)
    
    def test_send_message_invalid_attachment(self, cerebras_client: Tuple[CerebrasClient, str]) -> None:
        """Test error handling when sending a message with an invalid attachment."""
        client, session_id = cerebras_client
        
        with pytest.raises(FileNotFoundError) as e:
            client.send_message(session_id, "Test message", ["nonexistent_file.txt"])
        
        assert "Attachment file not found" in str(e.value)
    
    def test_network_timeout(self, cerebras_client: Tuple[CerebrasClient, str]) -> None:
        """Test error handling when the API request times out."""
        client, session_id = cerebras_client
        
        with patch('requests.post') as mock_post:
            mock_post.side_effect = Timeout("Request timed out")
            
            with pytest.raises(RuntimeError) as e:
                client.send_message(session_id, "Test message")
            
            assert "timed out" in str(e.value)
    
    def test_network_connection_error(self, cerebras_client: Tuple[CerebrasClient, str]) -> None:
        """Test error handling when a connection error occurs."""
        client, session_id = cerebras_client
        
        with patch('requests.post') as mock_post:
            mock_post.side_effect = ConnectionError("Connection error")
            
            with pytest.raises(RuntimeError) as e:
                client.send_message(session_id, "Test message")
            
            assert "Failed to connect" in str(e.value)
    
    def test_api_auth_error(self, cerebras_client: Tuple[CerebrasClient, str]) -> None:
        """Test error handling when an authentication error occurs."""
        client, session_id = cerebras_client
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_post.return_value = mock_response
            
            with pytest.raises(RuntimeError) as e:
                client.send_message(session_id, "Test message")
            
            assert "Authentication failed" in str(e.value)
    
    def test_api_rate_limit(self, cerebras_client: Tuple[CerebrasClient, str]) -> None:
        """Test error handling when a rate limit error occurs."""
        client, session_id = cerebras_client
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 429
            mock_post.return_value = mock_response
            
            with pytest.raises(RuntimeError) as e:
                client.send_message(session_id, "Test message")
            
            assert "Rate limit exceeded" in str(e.value)
    
    def test_api_server_error(self, cerebras_client: Tuple[CerebrasClient, str]) -> None:
        """Test error handling when a server error occurs."""
        client, session_id = cerebras_client
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_post.return_value = mock_response
            
            with pytest.raises(RuntimeError) as e:
                client.send_message(session_id, "Test message")
            
            assert "server error" in str(e.value)
    
    def test_invalid_json_response(self, cerebras_client: Tuple[CerebrasClient, str]) -> None:
        """Test error handling when an invalid JSON response is received."""
        client, session_id = cerebras_client
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_post.return_value = mock_response
            
            with pytest.raises(RuntimeError) as e:
                client.send_message(session_id, "Test message")
            
            assert "Invalid JSON" in str(e.value)
    
    def test_malformed_response(self, cerebras_client: Tuple[CerebrasClient, str]) -> None:
        """Test error handling when a malformed response is received."""
        client, session_id = cerebras_client
        
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            # Missing 'choices' in the response
            mock_response.json.return_value = {"usage": {"total_tokens": 10}}
            mock_post.return_value = mock_response
            
            with pytest.raises(RuntimeError) as e:
                client.send_message(session_id, "Test message")
            
            assert "Invalid response format" in str(e.value)
    
    def test_start_new_session_empty_user_id(self) -> None:
        """Test error handling when starting a session with an empty user ID."""
        with patch.dict(os.environ, {"CEREBRAS_API_KEY": "test-key"}):
            client = CerebrasClient()
            
            with pytest.raises(ValueError) as e:
                client.start_new_session("")
            
            assert "User ID cannot be empty" in str(e.value)
            
            with pytest.raises(ValueError) as e:
                client.start_new_session("   ")
            
            assert "User ID cannot be empty" in str(e.value)
    
    def test_start_new_session_invalid_model(self) -> None:
        """Test error handling when starting a session with an invalid model."""
        with patch.dict(os.environ, {"CEREBRAS_API_KEY": "test-key"}):
            client = CerebrasClient()
            
            # Override list_available_models to return a limited set
            client.list_available_models = lambda: [{"id": "valid-model"}]
            
            with pytest.raises(ValueError) as e:
                client.start_new_session("test-user", "invalid-model")
            
            assert "not available" in str(e.value)
            assert "valid-model" in str(e.value)
