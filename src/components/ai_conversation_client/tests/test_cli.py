"""Tests for the Cerebras AI CLI functionality."""

import io
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

import pytest

from src.components.ai_conversation_client.cli import (
    display_metrics,
    format_ai_response,
    main,
)


class TestCliFormat(unittest.TestCase):
    """Test suite for CLI formatting functions."""

    def test_format_ai_response(self) -> None:
        """Test the formatting of AI responses for terminal display."""
        # Test markdown headers
        md_text = "# This is a header\nRegular text\n## Subheader"
        formatted = format_ai_response(md_text)
        assert "THIS IS A HEADER" in formatted
        assert "SUBHEADER" in formatted
        assert "=====" in formatted  # Check for header underline

        # Test bold and italic formatting
        md_text = "This is **bold** and *italic* text"
        formatted = format_ai_response(md_text)
        assert "\033[1m" in formatted  # ANSI code for bold
        assert "\033[3m" in formatted  # ANSI code for italic

        # Test code blocks
        md_text = "```python\nprint('hello')\n```\nAnd `inline code`"
        formatted = format_ai_response(md_text)
        assert "\033[90m" in formatted  # ANSI code for gray
        assert "print('hello')" in formatted

        # Test list formatting
        md_text = "* Item 1\n* Item 2\n1. Numbered item"
        formatted = format_ai_response(md_text)
        assert "  • Item 1" in formatted
        assert "  1. Numbered item" in formatted

    def test_display_metrics(self) -> None:
        """Test the display of usage metrics."""
        metrics = {"token_count": 1234, "api_calls": 5, "cost_estimate": 0.01234}

        # Capture stdout to verify output
        with patch("sys.stdout", new=io.StringIO()) as fake_stdout:
            display_metrics(metrics)
            output = fake_stdout.getvalue()

            assert "Token count: 1,234" in output
            assert "API calls: 5" in output
            assert "Cost estimate: $0.01234" in output


@pytest.fixture
def mock_cerebras_client() -> MagicMock:
    """Create a mock CerebrasClient for testing CLI commands."""
    with patch(
        "src.components.ai_conversation_client.cli.CerebrasClient"
    ) as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        # Set up mock responses
        mock_client.list_available_models.return_value = [
            {
                "id": "test-model",
                "name": "Test Model",
                "capabilities": ["text-generation", "chat"],
                "max_tokens": 8192,
            }
        ]

        mock_client.start_new_session.return_value = "test-session-id"

        mock_client.send_message.return_value = {
            "response": "Test response",
            "attachments": [],
            "timestamp": "2023-01-01T00:00:00",
        }

        mock_client.get_usage_metrics.return_value = {
            "token_count": 100,
            "api_calls": 1,
            "cost_estimate": 0.001,
        }

        mock_client.summarize_conversation.return_value = "Test summary"

        mock_client.export_chat_history.return_value = '{"messages": []}'

        yield mock_client


class TestCliCommands:
    """Test suite for CLI commands."""

    def test_models_command(self, mock_cerebras_client: MagicMock) -> None:
        """Test the 'models' command."""
        test_args = ["cli.py", "models"]
        with (
            patch.object(sys, "argv", test_args),
            patch("sys.stdout", new=io.StringIO()) as fake_stdout,
            patch.dict(os.environ, {"CEREBRAS_API_KEY": "test-api-key"}),
        ):
            main()

            output = fake_stdout.getvalue()
            assert "Available models:" in output
            assert "Test Model" in output
            assert "test-model" in output

            mock_cerebras_client.list_available_models.assert_called_once()

    def test_metrics_command(self, mock_cerebras_client: MagicMock) -> None:
        """Test the 'metrics' command."""
        test_args = ["cli.py", "metrics", "test-session-id"]
        with (
            patch.object(sys, "argv", test_args),
            patch("sys.stdout", new=io.StringIO()) as fake_stdout,
            patch.dict(os.environ, {"CEREBRAS_API_KEY": "test-api-key"}),
        ):
            # Mock internal session tracking
            mock_cerebras_client._sessions = {"test-session-id": {"history": []}}

            main()

            output = fake_stdout.getvalue()
            assert "Token count:" in output

            mock_cerebras_client.get_usage_metrics.assert_called_once_with(
                "test-session-id"
            )

    def test_export_command(self, mock_cerebras_client: MagicMock) -> None:
        """Test the 'export' command."""
        test_args = ["cli.py", "export", "test-session-id", "--format", "json"]
        with (
            patch.object(sys, "argv", test_args),
            patch("sys.stdout", new=io.StringIO()) as fake_stdout,
            patch.dict(os.environ, {"CEREBRAS_API_KEY": "test-api-key"}),
        ):
            # Mock internal session tracking
            mock_cerebras_client._sessions = {"test-session-id": {"history": []}}

            main()

            output = fake_stdout.getvalue()
            assert '{"messages": []}' in output

            mock_cerebras_client.export_chat_history.assert_called_once_with(
                "test-session-id", "json"
            )

    def test_summarize_command(self, mock_cerebras_client: MagicMock) -> None:
        """Test the 'summarize' command."""
        test_args = ["cli.py", "summarize", "test-session-id"]
        with (
            patch.object(sys, "argv", test_args),
            patch("sys.stdout", new=io.StringIO()) as fake_stdout,
            patch.dict(os.environ, {"CEREBRAS_API_KEY": "test-api-key"}),
        ):
            # Mock internal session tracking
            mock_cerebras_client._sessions = {"test-session-id": {"history": []}}

            main()

            output = fake_stdout.getvalue()
            assert "Test summary" in output

            mock_cerebras_client.summarize_conversation.assert_called_once_with(
                "test-session-id"
            )

    def test_missing_api_key(self, mock_cerebras_client: MagicMock) -> None:
        """Test error handling when API key is missing."""
        test_args = ["cli.py", "models"]
        with (
            patch.object(sys, "argv", test_args),
            patch("sys.stdout", new=io.StringIO()) as fake_stdout,
            patch.dict(os.environ, {}, clear=True),
            patch("os.path.exists", return_value=False),
            patch("sys.exit") as mock_exit,
        ):  # Mock sys.exit to prevent test from actually exiting
            main()

            # Check that the error message is printed
            output = fake_stdout.getvalue()
            assert "CEREBRAS_API_KEY environment variable is required" in output

            # Verify that sys.exit was called with exit code 1
            mock_exit.assert_called_once_with(1)

    def test_session_not_found(self, mock_cerebras_client: MagicMock) -> None:
        """Test error handling when session ID is not found."""
        test_args = ["cli.py", "metrics", "nonexistent-session-id"]
        with (
            patch.object(sys, "argv", test_args),
            patch("sys.stdout", new=io.StringIO()) as fake_stdout,
            patch.dict(os.environ, {"CEREBRAS_API_KEY": "test-api-key"}),
            patch("sys.exit") as mock_exit,
        ):  # Mock sys.exit to prevent test from actually exiting
            # Mock internal session tracking with empty sessions
            mock_cerebras_client._sessions = {}

            main()

            # Check that the error message is printed
            output = fake_stdout.getvalue()
            assert "not found" in output

            # Verify that sys.exit was called with exit code 1
            mock_exit.assert_called_once_with(1)
