from unittest.mock import Mock
from src.components.ai_conversation_client import AIConversationClient

def test_interface_contracts():
    mock = Mock(spec=AIConversationClient)
    mock.send_message.return_value = "test"
    assert mock.send_message("hello") == "test"
    
    mock.get_history.return_value = [{"id": "1"}]
    assert isinstance(mock.get_history("sess1"), list)