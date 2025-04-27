"""Unit tests for the AIConversationClientInterface contract.

These tests validate a mock implementation of the AIConversationClientInterface.
"""

from datetime import datetime
from typing import cast
from unittest.mock import Mock, create_autospec

import pytest
from components.ai_conversation_client.interface import AIConversationClientInterface


@pytest.fixture
def mock_interface() -> AIConversationClientInterface:
    """
    Fixture to create a mock AIConversationClientInterface instance.

    Returns:
        A mock object adhering to the AIConversationClientInterface.
    """
    mock = create_autospec(AIConversationClientInterface, instance=True)
    return cast(AIConversationClientInterface, mock)


def test_send_message_contract(mock_interface: AIConversationClientInterface) -> None:
    """Verify that send_message returns dict containing 'response' and 'timestamp'."""
    test_response = {
        "response": "Hello, user!",
        "attachments": [],
        "timestamp": datetime.now(),
    }
    cast(Mock, mock_interface).send_message.return_value = test_response

    result = mock_interface.send_message("sess1", "Hi there!")
    assert isinstance(result, dict)
    assert "response" in result
    assert "timestamp" in result


def test_get_chat_history_contract(
    mock_interface: AIConversationClientInterface,
) -> None:
    """Verify that get_chat_history returns a list of messages with required fields."""
    mock_history = [
        {"id": "msg1", "content": "Hi", "sender": "user", "timestamp": datetime.now()},
        {
            "id": "msg2",
            "content": "Hello!",
            "sender": "ai",
            "timestamp": datetime.now(),
        },
    ]
    cast(Mock, mock_interface).get_chat_history.return_value = mock_history

    history = mock_interface.get_chat_history("sess1")
    assert isinstance(history, list)
    assert all(
        "id" in m and "content" in m and "sender" in m and "timestamp" in m
        for m in history
    )


def test_start_new_session_contract(
    mock_interface: AIConversationClientInterface,
) -> None:
    """Verify that start_new_session returns a valid session ID as a string."""
    cast(Mock, mock_interface).start_new_session.return_value = "sess123"
    session_id = mock_interface.start_new_session("user123", model="gpt-4")
    assert isinstance(session_id, str)
    assert len(session_id) > 0


def test_end_session_contract(mock_interface: AIConversationClientInterface) -> None:
    """Verify that end_session returns a boolean status."""
    cast(Mock, mock_interface).end_session.return_value = True
    assert mock_interface.end_session("sess123") is True


def test_list_available_models_contract(
    mock_interface: AIConversationClientInterface,
) -> None:
    """Verify list_available_models returns a list of models with required fields."""
    cast(Mock, mock_interface).list_available_models.return_value = [
        {"id": "gpt-4", "name": "GPT-4", "capabilities": ["chat"], "max_tokens": 4096}
    ]
    models = mock_interface.list_available_models()
    assert isinstance(models, list)
    assert all("id" in m and "name" in m for m in models)


def test_switch_model_contract(mock_interface: AIConversationClientInterface) -> None:
    """Verify that switch_model returns True when model switch is acknowledged."""
    cast(Mock, mock_interface).switch_model.return_value = True
    assert mock_interface.switch_model("sess123", "gpt-3")


def test_attach_file_contract(mock_interface: AIConversationClientInterface) -> None:
    """Verify that attach_file returns True when file is successfully attached."""
    cast(Mock, mock_interface).attach_file.return_value = True
    result = mock_interface.attach_file(
        "sess1", "/path/to/file.txt", description="example"
    )
    assert result is True


def test_get_usage_metrics_contract(
    mock_interface: AIConversationClientInterface,
) -> None:
    """Verify that get_usage_metrics returns expected metric keys and correct types."""
    cast(Mock, mock_interface).get_usage_metrics.return_value = {
        "token_count": 1000,
        "api_calls": 15,
        "cost_estimate": 0.12,
    }
    metrics = mock_interface.get_usage_metrics("sess123")
    assert "token_count" in metrics
    assert isinstance(metrics["token_count"], int)


def test_summarize_conversation_contract(
    mock_interface: AIConversationClientInterface,
) -> None:
    """Verify that summarize_conversation returns a non-empty summary string."""
    cast(Mock, mock_interface).summarize_conversation.return_value = (
        "Summary of conversation"
    )
    result = mock_interface.summarize_conversation("sess123")
    assert isinstance(result, str)
    assert result.startswith("Summary")


def test_export_chat_history_contract(
    mock_interface: AIConversationClientInterface,
) -> None:
    """Verify that export_chat_history returns a valid path ending with '.json'."""
    cast(Mock, mock_interface).export_chat_history.return_value = "/tmp/chat.json"
    path = mock_interface.export_chat_history("sess123", format="json")
    assert path.endswith(".json")
