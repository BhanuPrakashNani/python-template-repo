"""Example usage of the AI Conversation Client.

This module demonstrates how to use the AI Conversation Client interface with
dependency injection through the factory pattern.
"""

import os
import sys
from dotenv import load_dotenv

from src.components.ai_conversation_client.factory import AIClientFactory


def main() -> None:
    """Run the example conversation."""
    # Load environment variables from .env file
    load_dotenv()

    # Print available clients
    print("Available AI clients:")
    for client_name in AIClientFactory.list_available_clients():
        print(f"- {client_name}")
    print()

    # Create an AI client using the factory (dependency injection)
    # The factory will use the CEREBRAS_API_KEY from environment variables
    try:
        # Use the factory to get an instance (dependency injection)
        client = AIClientFactory.create_client("cerebras")
    except ValueError as e:
        print(f"Error: {e}")
        print("Make sure you have set the CEREBRAS_API_KEY environment variable.")
        sys.exit(1)

    # List available models
    print("Available models:")
    models = client.list_available_models()
    for model in models:
        print(f"- {model['name']} ({model['id']})")
    print()

    # Start a new session
    user_id = "example_user"
    session_id = client.start_new_session(user_id)
    print(f"Started new session: {session_id}")

    # Send messages in a loop
    try:
        while True:
            # Get user input
            user_message = input("\nYou: ")
            if user_message.lower() in ("exit", "quit", "bye"):
                break

            # Send the message to the AI
            print("Sending message to AI...")
            response = client.send_message(session_id, user_message)
            
            # Print the response
            print(f"\nAI: {response['response']}")
            
            # Print usage metrics after each message
            metrics = client.get_usage_metrics(session_id)
            print(
                f"\nUsage metrics - Tokens: {metrics['token_count']}, "
                f"API calls: {metrics['api_calls']}, "
                f"Est. cost: ${metrics['cost_estimate']:.4f}"
            )

    except KeyboardInterrupt:
        print("\nExiting conversation...")
    
    # End the session
    client.end_session(session_id)
    print(f"Ended session: {session_id}")
    
    # Summarize the conversation
    print("\nGenerating conversation summary...")
    summary = client.summarize_conversation(session_id)
    print(f"Summary: {summary}")
    
    # Export the conversation
    print("\nExporting conversation...")
    json_export = client.export_chat_history(session_id, format="json")
    export_path = f"conversation_{session_id}.json"
    with open(export_path, "w") as f:
        f.write(json_export)
    print(f"Conversation exported to {export_path}")


if __name__ == "__main__":
    main()
