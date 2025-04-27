"""Mock implementation of the AI Conversation Client interface for testing.

This module provides a mock implementation of the AIConversationClient interface
that can be used for testing without making actual API calls.
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Union

from src.components.ai_conversation_client.api import AIConversationClient
from src.components.ai_conversation_client.factory import AIClientFactory


class MockAIClient(AIConversationClient):
    """Mock implementation of AIConversationClient for testing.

    This class provides a complete implementation of the AIConversationClient interface
    that doesn't make any external API calls, suitable for testing.
    """

    # Pre-defined mock responses for testing
    MOCK_RESPONSES = [
        "I'm a mock AI assistant helping you test your code.",
        "This is a test response from the mock AI system.",
        "Your test is working correctly if you see this message.",
        "Mock AI systems are useful for testing without API costs.",
        "This is a simulated response that doesn't use a real AI API.",
    ]

    # Available mock models
    AVAILABLE_MODELS = [
        {
            "id": "mock-gpt-4",
            "name": "Mock GPT-4",
            "capabilities": ["text-generation", "chat"],
            "max_tokens": 8192,
        },
        {
            "id": "mock-gpt-3",
            "name": "Mock GPT-3.5",
            "capabilities": ["text-generation", "chat"],
            "max_tokens": 4096,
        },
        {
            "id": "mock-small",
            "name": "Mock Small Model",
            "capabilities": ["text-generation"],
            "max_tokens": 2048,
        },
    ]

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize a new mock AI conversation client instance.

        Args:
            api_key: Optional API key (not actually used but included for 
                interface compatibility).
        """
        self.api_key = api_key or "mock-api-key"
        self._sessions: Dict[str, Dict] = {}
        self._response_index = 0
        self._custom_responses: Dict[str, str] = {}

    def send_message(
        self, session_id: str, message: str, attachments: Optional[List[str]] = None
    ) -> Dict[str, Union[str, List[str], datetime]]:
        """Send a message to the mock AI and get a pre-defined response.

        Args:
            session_id: Unique identifier for the conversation session.
            message: The text message to send to the AI.
            attachments: Optional list of file paths or URLs (not actually used).

        Returns:
            Dictionary containing:
                - response: A pre-defined mock response
                - attachments: Empty list
                - timestamp: Current time

        Raises:
            ValueError: If the session_id does not exist.
        """
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        # Get the session data
        session = self._sessions[session_id]

        # Add user message to history
        msg_id = str(uuid.uuid4())
        timestamp = datetime.now()
        session["history"].append(
            {
                "id": msg_id,
                "content": message,
                "sender": "user",
                "timestamp": timestamp,
            }
        )

        # Generate mock response
        if message in self._custom_responses:
            # Use custom response if one is defined for this message
            response = self._custom_responses[message]
        else:
            # Use next pre-defined response
            response = self.MOCK_RESPONSES[self._response_index]
            self._response_index = (self._response_index + 1) % len(self.MOCK_RESPONSES)

        # Add AI response to history
        ai_msg_id = str(uuid.uuid4())
        ai_timestamp = datetime.now()
        session["history"].append(
            {
                "id": ai_msg_id,
                "content": response,
                "sender": "assistant",
                "timestamp": ai_timestamp,
            }
        )

        # Update metrics
        if "metrics" not in session:
            session["metrics"] = {
                "token_count": 0,
                "api_calls": 0,
                "cost_estimate": 0.0,
            }

        # Simulate token counting (very simple approximation)
        estimated_tokens = len(message.split()) + len(response.split())
        session["metrics"]["token_count"] += estimated_tokens
        session["metrics"]["api_calls"] += 1
        session["metrics"]["cost_estimate"] += estimated_tokens * 0.0001  # Fake cost

        return {
            "response": response,
            "attachments": [],
            "timestamp": ai_timestamp,
        }

    def get_chat_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[Dict[str, Union[str, datetime]]]:
        """Retrieve conversation history for a session.

        Args:
            session_id: Unique identifier for the conversation session.
            limit: Maximum number of messages to retrieve.

        Returns:
            List of message dictionaries.

        Raises:
            ValueError: If the session_id does not exist.
        """
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        history = self._sessions[session_id]["history"]

        if limit is not None:
            history = history[-limit:]

        return history

    def start_new_session(self, user_id: str, model: Optional[str] = None) -> str:
        """Start a new conversation session.

        Args:
            user_id: Unique identifier for the user.
            model: Optional model identifier to use.

        Returns:
            New session identifier.

        Raises:
            ValueError: If the specified model is not available.
        """
        # Use default model if none specified
        model = model or "mock-gpt-4"

        # Check if model is available
        available_model_ids = [m["id"] for m in self.AVAILABLE_MODELS]
        if model not in available_model_ids:
            raise ValueError(
                f"Model {model} is not available. "
                f"Available models: {', '.join(available_model_ids)}"
            )

        # Generate a unique session ID
        session_id = str(uuid.uuid4())

        # Create a new session
        self._sessions[session_id] = {
            "user_id": user_id,
            "model": model,
            "history": [],
            "active": True,
            "created_at": datetime.now(),
        }

        return session_id

    def end_session(self, session_id: str) -> bool:
        """End an active conversation session.

        Args:
            session_id: Session identifier to end.

        Returns:
            True if session was ended successfully, False otherwise.
        """
        if session_id not in self._sessions:
            return False

        self._sessions[session_id]["active"] = False
        return True

    def list_available_models(self) -> List[Dict[str, Union[str, List[str], int, bool]]]:
        """Get available mock AI models.

        Returns:
            List of model dictionaries.
        """
        return self.AVAILABLE_MODELS

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
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        session = self._sessions[session_id]

        # Check if model is available
        available_model_ids = [m["id"] for m in self.AVAILABLE_MODELS]
        if model_id not in available_model_ids:
            raise ValueError(
                f"Model {model_id} is not available. "
                f"Available models: {', '.join(available_model_ids)}"
            )

        # Switch the model
        session["model"] = model_id
        return True

    def attach_file(
        self, session_id: str, file_path: str, description: Optional[str] = None
    ) -> bool:
        """Simulate attaching a file to the conversation context.

        Args:
            session_id: Active session identifier.
            file_path: Path to the file.
            description: Optional description of the file.

        Returns:
            True if file was attached successfully, False otherwise.

        Raises:
            ValueError: If the session_id does not exist.
            FileNotFoundError: If the file doesn't exist.
        """
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Mock successful attachment
        if "attachments" not in self._sessions[session_id]:
            self._sessions[session_id]["attachments"] = []

        self._sessions[session_id]["attachments"].append(
            {
                "path": file_path,
                "description": description,
                "timestamp": datetime.now(),
            }
        )

        return True

    def get_usage_metrics(self, session_id: str) -> Dict[str, Union[int, float]]:
        """Get usage statistics for a session.

        Args:
            session_id: Session identifier to check.

        Returns:
            Dictionary containing mock usage metrics.

        Raises:
            ValueError: If the session_id does not exist.
        """
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        if "metrics" not in self._sessions[session_id]:
            # Return empty metrics if none exist yet
            return {
                "token_count": 0,
                "api_calls": 0,
                "cost_estimate": 0.0,
            }

        return self._sessions[session_id]["metrics"]

    def summarize_conversation(self, session_id: str) -> str:
        """Generate a mock summary of the conversation.

        Args:
            session_id: Session identifier for conversation to summarize.

        Returns:
            Mock summary of the conversation.

        Raises:
            ValueError: If the session_id does not exist.
        """
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        if not self._sessions[session_id]["history"]:
            return "No conversation to summarize."

        # Generate a very simple mock summary
        user_messages = [
            msg["content"]
            for msg in self._sessions[session_id]["history"]
            if msg["sender"] == "user"
        ]

        user_message_count = len(user_messages)
        ai_message_count = len(
            [
                msg
                for msg in self._sessions[session_id]["history"]
                if msg["sender"] == "assistant"
            ]
        )

        return (
            f"This conversation contains {user_message_count} user messages and "
            f"{ai_message_count} AI responses. The user asked about: "
            f"{', '.join(user_messages[:2])}..."
        )

    def export_chat_history(self, session_id: str, format: str = "json") -> str:
        """Export chat history to a specified format.

        Args:
            session_id: Session identifier for the conversation.
            format: Format to export the chat history ('json' or 'txt').

        Returns:
            String representation of the chat history.

        Raises:
            ValueError: If the session_id does not exist or the format is unsupported.
        """
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        history = self._sessions[session_id]["history"]

        if format.lower() == "json":
            # Export as JSON
            export_data = {
                "session_id": session_id,
                "user_id": self._sessions[session_id]["user_id"],
                "model": self._sessions[session_id]["model"],
                "created_at": self._sessions[session_id]["created_at"].isoformat(),
                "messages": [
                    {
                        "id": msg["id"],
                        "content": msg["content"],
                        "sender": msg["sender"],
                        "timestamp": msg["timestamp"].isoformat(),
                    }
                    for msg in history
                ],
            }
            return json.dumps(export_data, indent=2)

        elif format.lower() == "txt":
            # Export as plain text
            output = f"Session ID: {session_id}\n"
            output += f"User ID: {self._sessions[session_id]['user_id']}\n"
            output += f"Model: {self._sessions[session_id]['model']}\n"
            output += f"Created: {self._sessions[session_id]['created_at'].isoformat()}\n\n"
            output += "Conversation:\n\n"

            for msg in history:
                sender = "User" if msg["sender"] == "user" else "AI"
                time_str = msg["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                output += f"[{time_str}] {sender}: {msg['content']}\n\n"

            return output

        else:
            raise ValueError(f"Unsupported export format: {format}. Supported formats: json, txt")

    # Testing-specific methods (not part of the interface)

    def set_custom_response(self, message: str, response: str) -> None:
        """Set a custom response for a specific message.

        Args:
            message: The message to respond to.
            response: The custom response to provide.
        """
        self._custom_responses[message] = response


# Register the mock client with the factory
AIClientFactory.register_client("mock", MockAIClient) 