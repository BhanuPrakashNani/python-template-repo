"""Test implementation of the AIConversationClient for integration tests."""

import uuid
from datetime import datetime
from typing import Any

from src.components.ai_conversation_client.cerebras_client import CerebrasClient
from src.components.ai_conversation_client.factory import AIClientFactory


class TestCerebrasClient(CerebrasClient):
    """Test implementation of CerebrasClient for integration and E2E tests.

    This client behaves like the real CerebrasClient but doesn't make actual API calls,
    allowing for deterministic testing of integration points without mocking.
    """

    def __init__(self, api_key: str = "test-api-key") -> None:
        """Initialize with test API key and configure test responses.

        Args:
            api_key: A dummy API key for testing.
        """
        super().__init__(api_key)

        # Set up pre-configured test responses
        self.test_responses = {
            "message": {
                "default": "This is a default test response.",
                "spam_analysis": {
                    "probability": "75",
                    "category": "Marketing"
                }
            },
            "summarize": "This is a test summary of the conversation.",
            "usage": {
                "total_tokens": 25
            }
        }

        # Enable deterministic behavior for testing
        self.next_responses = []

    def configure_responses(self, responses: list[dict[str, Any]]) -> None:
        """Configure a sequence of responses to be returned by send_message.

        Args:
            responses: A list of response dictionaries.
        """
        self.next_responses = responses

    def send_message(
        self, session_id: str, message: str, attachments: list[str] | None = None
    ) -> dict[str, Any]:
        """Simulate sending a message without making an API call.

        Args:
            session_id: The session identifier.
            message: The message text to send.
            attachments: Optional list of file paths (not used).

        Returns:
            A response dictionary similar to the real client.

        Raises:
            ValueError: If the session doesn't exist.
        """
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        session = self._sessions[session_id]

        # Add user message to history
        message_id = str(uuid.uuid4())
        session["history"].append({
            "id": message_id,
            "content": message,
            "sender": "user",
            "timestamp": datetime.now()
        })

        # Use configured responses if available
        if self.next_responses:
            response_text = self.next_responses.pop(0).get(
                "response", self.test_responses["message"]["default"]
            )
        elif "spam" in message.lower() and "probability" in message.lower():
            # For spam analysis: return probability
            response_text = self.test_responses["message"]["spam_analysis"][
                "probability"
            ]
        elif "spam" in message.lower() and "category" in message.lower():
            # For spam categories
            response_text = self.test_responses["message"]["spam_analysis"]["category"]
        else:
            # Default response
            response_text = self.test_responses["message"]["default"]

        # Add assistant response to history
        response_id = str(uuid.uuid4())
        session["history"].append({
            "id": response_id,
            "content": response_text,
            "sender": "assistant",
            "timestamp": datetime.now()
        })

        # Update usage metrics
        if "metrics" not in session:
            session["metrics"] = {
                "token_count": 0,
                "api_calls": 0,
                "cost_estimate": 0.0
            }

        tokens = self.test_responses["usage"]["total_tokens"]
        session["metrics"]["token_count"] += tokens
        session["metrics"]["api_calls"] += 1
        session["metrics"]["cost_estimate"] += (tokens / 1000) * 0.01

        # Return a response object like the real client would
        return {
            "response": response_text,
            "attachments": [],
            "timestamp": datetime.now()
        }

    def summarize_conversation(self, session_id: str) -> str:
        """Simulate summarizing a conversation without making an API call.

        Args:
            session_id: The session identifier.

        Returns:
            A predetermined summary response.

        Raises:
            ValueError: If the session doesn't exist.
        """
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        session = self._sessions[session_id]

        # Check if there's enough content to summarize
        if len(session["history"]) < 2:
            return "Not enough conversation to summarize."

        # Update metrics
        if "metrics" not in session:
            session["metrics"] = {
                "token_count": 0,
                "api_calls": 0,
                "cost_estimate": 0.0
            }

        tokens = 30  # Simulated token count
        session["metrics"]["token_count"] += tokens
        session["metrics"]["api_calls"] += 1
        session["metrics"]["cost_estimate"] += (tokens / 1000) * 0.01

        return self.test_responses["summarize"]


# Register with the factory
AIClientFactory.register_client("test", TestCerebrasClient)
