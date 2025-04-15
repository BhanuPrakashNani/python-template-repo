"""Cerebras implementation of the AI Conversation Client interface.

This module implements the AIConversationClient interface for the Cerebras API.
"""

import json
import os
import uuid
from datetime import datetime
from typing import Any, cast

import requests

from src.components.ai_conversation_client.api import AIConversationClient


class CerebrasClient(AIConversationClient):
    """Cerebras implementation of the AIConversationClient interface.

    This class provides a concrete implementation of the AIConversationClient interface
    using direct HTTP requests to the Cerebras API.
    """

    # Base API URL for Cerebras
    API_BASE_URL = "https://api.cerebras.ai/v1"

    # Available Cerebras models according to the documentation
    AVAILABLE_MODELS = [
        {
            "id": "llama-4-scout-17b-16e-instruct",
            "name": "Llama 4 Scout",
            "capabilities": ["text-generation", "chat"],
            "max_tokens": 8192,
            "knowledge_cutoff": "August 2024",
        },
        {
            "id": "llama3.1-8b",
            "name": "Llama 3.1 8B",
            "capabilities": ["text-generation", "chat"],
            "max_tokens": 8192,
            "knowledge_cutoff": "March 2023",
        },
        {
            "id": "llama-3.3-70b",
            "name": "Llama 3.3 70B",
            "capabilities": ["text-generation", "chat"],
            "max_tokens": 8192,
            "knowledge_cutoff": "December 2023",
        },
        {
            "id": "deepseek-r1-distill-llama-70b",
            "name": "DeepSeek R1 Distill Llama 70B",
            "capabilities": ["text-generation", "chat"],
            "max_tokens": 8192,
            "knowledge_cutoff": "December 2023",
            "private_preview": True,
        },
    ]

    def __init__(self, api_key: str | None = None) -> None:
        """Initialize a new Cerebras AI conversation client instance.

        # fmt: off

        Args:
            api_key: API key for authentication with the Cerebras service.
                If not provided, attempts to read from CEREBRAS_API_KEY environment variable.  # noqa
        # fmt: on
        """
        self.api_key = api_key or os.environ.get("CEREBRAS_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Cerebras API key must be provided either as a parameter or "
                "via the CEREBRAS_API_KEY environment variable."
            )

        # Dictionary to store active conversation sessions
        self._sessions: dict[str, dict[str, Any]] = {}

        # Headers for API requests
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def send_message(
        self, session_id: str, message: str, attachments: list[str] | None = None
    ) -> dict[str, str | list[str] | datetime]:
        """Send a message to the Cerebras AI service and get a response.

        # fmt: off

        Args:
            session_id: Unique identifier for the conversation session.
            message: The text message to send to the AI.
            attachments: Optional list of file paths or URLs to include (not supported yet).  # noqa

        Returns:
            Dictionary containing:
                - response: The AI's text response
                - attachments: List of generated files (empty list for now)
                - timestamp: When the response was generated

        Raises:
            ValueError: If the session_id does not exist.
            RuntimeError: If the API request fails.
        # fmt: on
        """
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        # Get the session data
        session = self._sessions[session_id]

        # Add the new message to the chat history
        msg_id = str(uuid.uuid4())
        timestamp = datetime.now()

        # Store the user message
        session["history"].append(
            {
                "id": msg_id,
                "content": message,
                "sender": "user",
                "timestamp": timestamp,
            }
        )

        # Prepare message history for the API
        messages = [
            {
                "role": "system" if msg["sender"] == "system" else msg["sender"],
                "content": msg["content"],
            }
            for msg in session["history"]
        ]

        # Prepare the API request
        url = f"{self.API_BASE_URL}/chat/completions"
        payload = {
            "model": session["model"],
            "messages": messages,
            "max_tokens": 1024,
        }

        # Make the API request
        try:
            response = requests.post(url, headers=self._headers, json=payload)
            response.raise_for_status()

            # Extract the response content
            response_data = response.json()
            ai_message = response_data["choices"][0]["message"]["content"]

            # Add the AI response to the chat history
            ai_msg_id = str(uuid.uuid4())
            ai_timestamp = datetime.now()

            session["history"].append(
                {
                    "id": ai_msg_id,
                    "content": ai_message,
                    "sender": "assistant",
                    "timestamp": ai_timestamp,
                }
            )

            # Update usage metrics
            if "usage" in response_data:
                if "metrics" not in session:
                    session["metrics"] = {
                        "token_count": 0,
                        "api_calls": 0,
                        "cost_estimate": 0.0,
                    }

                session["metrics"]["token_count"] += response_data["usage"][
                    "total_tokens"
                ]
                session["metrics"]["api_calls"] += 1
                # Pricing estimate based on token usage
                session["metrics"]["cost_estimate"] += (
                    response_data["usage"]["total_tokens"] / 1000
                ) * 0.01

            # Return the response
            return {
                "response": ai_message,
                "attachments": [],
                "timestamp": ai_timestamp,
            }

        except requests.RequestException as e:
            raise RuntimeError(f"Failed to send message to Cerebras API: {str(e)}")

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

        Raises:
            ValueError: If the session_id does not exist.
        """
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        history = self._sessions[session_id]["history"]

        if limit is not None:
            history = history[-limit:]

        # Ensure we return the right type
        return cast(list[dict[str, str | datetime]], history)

    def start_new_session(self, user_id: str, model: str | None = None) -> str:
        """Start a new conversation session.

        # fmt: off

        Args:
            user_id: Unique identifier for the user.
            model: Optional model identifier to use. Defaults to "llama-4-scout-17b-16e-instruct".  # noqa

        Returns:
            New session identifier.

        Raises:
            ValueError: If the specified model is not available.
        # fmt: on
        """
        # Use default model if none specified
        model = model or "llama-4-scout-17b-16e-instruct"

        # Check if model is available
        available_model_ids = [m["id"] for m in self.AVAILABLE_MODELS]
        if model not in available_model_ids:
            raise ValueError(
                f"Model {model} is not available. "
                f"Available models: {', '.join(cast(list[str], available_model_ids))}"
            )

        # Create a new session
        session_id = str(uuid.uuid4())

        self._sessions[session_id] = {
            "user_id": user_id,
            "model": model,
            "history": [],
            "created_at": datetime.now(),
            "active": True,
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

    def list_available_models(
        self,
    ) -> list[dict[str, str | list[str] | int | bool]]:
        """Get available Cerebras AI models with their capabilities.

        Returns:
            List of model dictionaries containing:
                - id: Model identifier
                - name: Human-readable name
                - capabilities: List of supported features
                - max_tokens: Maximum context length
        """
        return cast(
            list[dict[str, str | list[str] | int | bool]], self.AVAILABLE_MODELS
        )

    def switch_model(self, session_id: str, model_id: str) -> bool:
        """Change the AI model for an active session.

        Args:
            session_id: Active session identifier.
            model_id: New model identifier to switch to.

        Returns:
            True if model was switched successfully, False otherwise.

        Raises:
            ValueError: If the specified model is not available.
        """
        if session_id not in self._sessions:
            return False

        # Check if model is available
        available_model_ids = [m["id"] for m in self.AVAILABLE_MODELS]
        if model_id not in available_model_ids:
            raise ValueError(
                f"Model {model_id} is not available. "
                f"Available models: {', '.join(cast(list[str], available_model_ids))}"
            )

        # Update the session model
        self._sessions[session_id]["model"] = model_id

        return True

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
        # Currently this is a stub implementation
        if session_id not in self._sessions:
            return False

        # Check if file exists
        if not os.path.exists(file_path):
            return False

        # Add file to session
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

    def get_usage_metrics(self, session_id: str) -> dict[str, int | float]:
        """Get usage statistics for a session.

        Args:
            session_id: Session identifier to check.

        Returns:
            Dictionary containing:
                - token_count: Total tokens used
                - api_calls: Number of API requests
                - cost_estimate: Estimated cost

        Raises:
            ValueError: If the session_id does not exist.
        """
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        # Return metrics or default values if not present
        metrics = self._sessions[session_id].get(
            "metrics",
            {
                "token_count": 0,
                "api_calls": 0,
                "cost_estimate": 0.0,
            },
        )

        return cast(dict[str, int | float], metrics)

    def summarize_conversation(self, session_id: str) -> str:
        """Generate summary of the entire conversation.

        This uses the Cerebras API to generate a summary of the conversation.

        Args:
            session_id: Session identifier for conversation to summarize.

        Returns:
            Summary of the conversation as a string.

        Raises:
            ValueError: If the session_id does not exist.
            RuntimeError: If the API request fails.
        """
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        # Get the session history
        history = self._sessions[session_id]["history"]

        if not history:
            return "No conversation to summarize."

        # Format the conversation history as a string
        conversation_text = "\n".join(
            [f"{msg['sender'].upper()}: {msg['content']}" for msg in history]
        )

        # Prepare a system message with summarization instruction
        summary_prompt = (
            f"Please summarize the following conversation:\n\n{conversation_text}"
        )

        # Prepare the API request
        url = f"{self.API_BASE_URL}/chat/completions"
        payload = {
            "model": self._sessions[session_id]["model"],
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes conversations.",  # noqa
                },
                {"role": "user", "content": summary_prompt},
            ],
            "max_tokens": 256,
            "temperature": 0.5,
        }

        # Make the API request
        try:
            response = requests.post(url, headers=self._headers, json=payload)
            response.raise_for_status()

            # Extract the summary
            response_data = response.json()
            summary = response_data["choices"][0]["message"]["content"].strip()

            # Update usage metrics
            if "usage" in response_data:
                if "metrics" not in self._sessions[session_id]:
                    self._sessions[session_id]["metrics"] = {
                        "token_count": 0,
                        "api_calls": 0,
                        "cost_estimate": 0.0,
                    }

                self._sessions[session_id]["metrics"]["token_count"] += response_data[
                    "usage"
                ]["total_tokens"]
                self._sessions[session_id]["metrics"]["api_calls"] += 1
                # Pricing estimate based on token usage
                self._sessions[session_id]["metrics"]["cost_estimate"] += (
                    response_data["usage"]["total_tokens"] / 1000
                ) * 0.01

            return summary

        except requests.RequestException as e:
            raise RuntimeError(
                f"Failed to generate summary using Cerebras API: {str(e)}"
            )

    def export_chat_history(self, session_id: str, format: str = "json") -> str:
        """Export chat history to a specified format.

        # fmt: off

        Args:
            session_id: Session identifier for the conversation.
            format: Format to export the chat history (currently only 'json' is supported).  # noqa

        Returns:
            String representation of the chat history in the specified format.

        Raises:
            ValueError: If the session_id does not exist or format is not supported.
        # fmt: on
        """
        if session_id not in self._sessions:
            raise ValueError(f"Session {session_id} does not exist")

        if format.lower() != "json":
            raise ValueError(
                f"Format {format} is not supported. Only 'json' is currently supported."
            )

        # Get the session history
        history = self._sessions[session_id]["history"]

        # Convert history to JSON format
        # Convert datetime objects to ISO format strings for JSON serialization
        serializable_history = []
        for msg in history:
            serialized_msg = {
                "id": msg["id"],
                "content": msg["content"],
                "sender": msg["sender"],
                "timestamp": msg["timestamp"].isoformat(),
            }
            serializable_history.append(serialized_msg)

        # Create the JSON data structure
        json_data = {
            "session_id": session_id,
            "user_id": self._sessions[session_id]["user_id"],
            "model": self._sessions[session_id]["model"],
            "created_at": self._sessions[session_id]["created_at"].isoformat(),
            "messages": serializable_history,
        }

        # Convert to JSON string and explicitly tell mypy it's a string
        json_str: str = json.dumps(json_data, indent=2)
        return json_str
