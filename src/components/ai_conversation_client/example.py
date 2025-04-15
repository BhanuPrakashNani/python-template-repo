"""Example usage of the CerebrasClient.

This script demonstrates how to use the CerebrasClient to interact with the Cerebras API.
"""

import os
import sys
from datetime import datetime
from typing import cast

from src.components.ai_conversation_client import CerebrasClient


def main() -> None:
    """Run a simple example interaction with the Cerebras AI service."""
    # Get API key from environment variable
    api_key = os.environ.get("CEREBRAS_API_KEY")

    if not api_key:
        print("Error: CEREBRAS_API_KEY environment variable is required.")
        sys.exit(1)

    try:
        # Initialize the client
        client = CerebrasClient(api_key=api_key)

        # List available models
        print("Available models:")
        models = client.list_available_models()
        for model in models:
            print(f"  - {model['name']} (ID: {model['id']})")
            # Convert capabilities to list of strings for safe joining
            capabilities = cast(list[str], model["capabilities"])
            print(f"    Capabilities: {', '.join(capabilities)}")
            print(f"    Max tokens: {model['max_tokens']}")
            print(
                f"    Knowledge cutoff: {model.get('knowledge_cutoff', 'Not specified')}"
            )
            if model.get("private_preview"):
                print(
                    "    Note: This model is in private preview. Contact Cerebras for access."
                )

        # Create a new session
        user_id = "example_user_001"
        model_id = "llama-4-scout-17b-16e-instruct"  # Using Llama 4 Scout model
        print(f"\nCreating session for user: {user_id}")
        session_id = client.start_new_session(user_id, model=model_id)
        print(f"Session created: {session_id}")

        # Send a message
        print(f"\nSending message to model: {model_id}...")
        message = "What are the latest developments in AI research?"
        response = client.send_message(session_id, message)

        print(f"\nUser: {message}")
        # Cast the timestamp to datetime for safe access to strftime
        response_time = cast(datetime, response["timestamp"])
        print(f"AI ({response_time.strftime('%H:%M:%S')}): {response['response']}")

        # Send a follow-up message
        print("\nSending follow-up message...")
        follow_up = "How do these developments impact society?"
        response = client.send_message(session_id, follow_up)

        print(f"\nUser: {follow_up}")
        # Cast the timestamp to datetime for safe access to strftime
        response_time = cast(datetime, response["timestamp"])
        print(f"AI ({response_time.strftime('%H:%M:%S')}): {response['response']}")

        # Get chat history
        print("\nChat history:")
        history = client.get_chat_history(session_id)
        for msg in history:
            # Cast to appropriate types for safe access
            timestamp = cast(datetime, msg["timestamp"]).strftime("%H:%M:%S")
            sender = cast(str, msg["sender"]).upper()
            content = cast(str, msg["content"])
            print(f"[{timestamp}] {sender}: {content}")

        # Get usage metrics
        print("\nUsage metrics:")
        metrics = client.get_usage_metrics(session_id)
        print(f"  Token count: {metrics['token_count']}")
        print(f"  API calls: {metrics['api_calls']}")
        print(f"  Cost estimate: ${metrics['cost_estimate']:.6f}")

        # Try a different model if available
        try:
            alternate_model = "llama3.1-8b"
            print(f"\nSwitching to model: {alternate_model}")
            if client.switch_model(session_id, alternate_model):
                print("Model switched successfully.")

                # Test message with new model
                print(f"\nSending message to model: {alternate_model}...")
                new_model_msg = (
                    "What are the best practices for fine-tuning large language models?"
                )
                response = client.send_message(session_id, new_model_msg)

                print(f"\nUser: {new_model_msg}")
                # Cast the timestamp to datetime for safe access to strftime
                response_time = cast(datetime, response["timestamp"])
                print(
                    f"AI ({response_time.strftime('%H:%M:%S')}): {response['response']}"
                )
        except ValueError as e:
            print(f"Could not switch model: {str(e)}")

        # Generate a summary
        print("\nGenerating conversation summary...")
        summary = client.summarize_conversation(session_id)
        print(f"Summary: {summary}")

        # Export chat history
        print("\nExporting chat history...")
        exported = client.export_chat_history(session_id)
        print(f"Exported history: {exported[:100]}...")  # Show first 100 chars

        # End session
        print("\nEnding session...")
        client.end_session(session_id)
        print("Session ended.")

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
