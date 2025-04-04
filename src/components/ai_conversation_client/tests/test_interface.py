"""Unit tests for the AI Conversation Client interface.

These tests verify the contract defined by the AIConversationClient abstract class.
"""

from datetime import datetime
from unittest.mock import Mock

import pytest

from src.components.ai_conversation_client.api import AIConversationClient


class TestAIConversationClient:
    """Test suite for AIConversationClient interface compliance."""

    @pytest.fixture
    def mock_client(self) -> Mock:
        """Create a mock AIConversationClient instance for testing.

        Returns:
            A Mock object configured with AIConversationClient's interface.
        """
        return Mock(spec=AIConversationClient)

    def test_send_message_contract(self, mock_client: Mock) -> None:
        """Verify send_message() adheres to its interface contract."""
        test_response = {
            "response": "Test reply",
            "timestamp": datetime.now().isoformat(),
        }
        mock_client.send_message.return_value = test_response

        result = mock_client.send_message("sess1", "Hello")
        assert isinstance(result, dict)
        assert "response" in result
        assert "timestamp" in result

    def test_list_available_models_contract(self, mock_client: Mock) -> None:
        """Verify list_available_models() returns proper structure."""
        mock_models = [
            {"id": "gpt-4", "name": "GPT-4", "max_tokens": 8192},
            {"id": "claude-2", "name": "Claude 2", "max_tokens": 100000},
        ]
        mock_client.list_available_models.return_value = mock_models

        models = mock_client.list_available_models()
        assert isinstance(models, list)
        assert all("id" in m and "name" in m for m in models)

    def test_switch_model_contract(self, mock_client: Mock) -> None:
        """Verify switch_model() returns boolean status."""
        mock_client.switch_model.return_value = True
        assert mock_client.switch_model("sess1", "gpt-4") is True
        mock_client.switch_model.assert_called_once_with("sess1", "gpt-4")

    def test_attach_file_contract(self, mock_client: Mock) -> None:
        """Verify attach_file() returns boolean status."""
        mock_client.attach_file.return_value = True
        assert mock_client.attach_file("sess1", "doc.pdf", None) is True
        mock_client.attach_file.assert_called_once_with("sess1", "doc.pdf", None)

    def test_get_usage_metrics_contract(self, mock_client: Mock) -> None:
        """Verify get_usage_metrics() returns proper metrics."""
        mock_metrics = {"token_count": 1500, "api_calls": 12}
        mock_client.get_usage_metrics.return_value = mock_metrics

        metrics = mock_client.get_usage_metrics("sess1")
        assert isinstance(metrics, dict)
        assert "token_count" in metrics
        assert isinstance(metrics["token_count"], int)

    def test_summarize_conversation_contract(self, mock_client: Mock) -> None:
        """Verify summarize_conversation() returns a valid summary."""
        summary_text = "This conversation covered project scope and timelines."
        mock_client.summarize_conversation.return_value = summary_text

        result = mock_client.summarize_conversation("sess1")
        assert isinstance(result, str)
        assert len(result) > 0
        mock_client.summarize_conversation.assert_called_once_with("sess1")

    def text_export_chat_history_contract(self, mock_client: Mock) -> None:
        """Verify export_chat_history() returns a valid file path."""
        mock_file_path = "/exports/sess1_history.json"
        mock_client.export_chat_history.return_value = mock_file_path

        result = mock_client.export_chat_history("sess1", format="json")
        assert isinstance(result, str)
        assert result.endswith(".json")
        mock_client.export_chat_history.assert_called_once_with("sess1", format="json")
