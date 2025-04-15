#!/usr/bin/env python
"""Command-line interface for the Cerebras AI Conversation Client."""

import argparse
import os
import re
import sys
from datetime import datetime
from typing import Any, cast

from src.components.ai_conversation_client import CerebrasClient


def format_ai_response(text: str) -> str:
    """Format AI response text for better terminal display.

    Args:
        text: The raw response text from the AI with markdown formatting.

    Returns:
        Formatted text for terminal display.
    """
    # Replace markdown headers with plain text headers
    text = re.sub(
        r"^#{1,6}\s+(.+?)$",
        lambda m: f"\n{m.group(1).upper()}\n{'=' * len(m.group(1))}\n",
        text,
        flags=re.MULTILINE,
    )

    # Replace bold/italic formatting
    text = re.sub(
        r"\*\*(.+?)\*\*", lambda m: f"\033[1m{m.group(1)}\033[0m", text
    )  # Bold
    text = re.sub(r"\*(.+?)\*", lambda m: f"\033[3m{m.group(1)}\033[0m", text)  # Italic

    # Format code blocks
    text = re.sub(
        r"```(?:\w+)?\n(.*?)\n```",
        lambda m: f"\n\033[90m{m.group(1)}\033[0m\n",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"`(.*?)`", lambda m: f"\033[90m{m.group(1)}\033[0m", text
    )  # Inline code

    # Format lists
    text = re.sub(
        r"^\*\s+(.+?)$", lambda m: f"  • {m.group(1)}", text, flags=re.MULTILINE
    )
    text = re.sub(
        r"^\d+\.\s+(.+?)$", lambda m: f"  {m.group(0)}", text, flags=re.MULTILINE
    )

    # Ensure proper spacing
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


def display_metrics(metrics: dict[str, Any]) -> None:
    """Format and display usage metrics.

    Args:
        metrics: Dictionary containing usage metrics.
    """
    print("\nUsage Metrics:")
    print(f"  Token count: {metrics['token_count']:,}")
    print(f"  API calls: {metrics['api_calls']}")
    print(f"  Cost estimate: ${metrics['cost_estimate']:.6f}")


def main() -> None:
    """Run the CLI interface."""
    parser = argparse.ArgumentParser(description="Cerebras AI Conversation Client CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Start a chat with the AI")
    chat_parser.add_argument(
        "--model", help="Model to use", default="llama-4-scout-17b-16e-instruct"
    )
    chat_parser.add_argument("--session-id", help="Continue an existing session")

    # List models command
    subparsers.add_parser("models", help="List available models")

    # List sessions command
    subparsers.add_parser("sessions", help="List active sessions")

    # Export command
    export_parser = subparsers.add_parser(
        "export", help="Export a session's chat history"
    )
    export_parser.add_argument("session_id", help="ID of the session to export")
    export_parser.add_argument(
        "--format", choices=["json", "text"], default="json", help="Export format"
    )
    export_parser.add_argument("--output", help="Output file path")

    # Metrics command
    metrics_parser = subparsers.add_parser(
        "metrics", help="Show usage metrics for a session"
    )
    metrics_parser.add_argument(
        "session_id", help="ID of the session to get metrics for"
    )

    # Summarize command
    summarize_parser = subparsers.add_parser(
        "summarize", help="Generate a summary of the conversation"
    )
    summarize_parser.add_argument("session_id", help="ID of the session to summarize")
    summarize_parser.add_argument("--output", help="Output file path")

    # Attach file command
    attach_parser = subparsers.add_parser(
        "attach", help="Attach a file to a conversation session"
    )
    attach_parser.add_argument("session_id", help="ID of the session to attach file to")
    attach_parser.add_argument("file_path", help="Path to the file to attach")
    attach_parser.add_argument("--description", help="Description of the file")

    # Parse arguments
    args = parser.parse_args()

    # Check for command
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Check for API key
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        # Try to load from .env.local file
        try:
            env_path = os.path.join(os.getcwd(), ".env.local")
            if os.path.exists(env_path):
                with open(env_path) as f:
                    for line in f:
                        if line.strip() and not line.startswith("#"):
                            key, value = line.strip().split("=", 1)
                            if key == "CEREBRAS_API_KEY":
                                api_key = value.strip().strip("\"'")
        except Exception:
            pass

    if not api_key:
        print("Error: CEREBRAS_API_KEY environment variable is required.")
        print("Please set it in your environment or in a .env.local file.")
        sys.exit(1)

    # Initialize client
    client = CerebrasClient(api_key=api_key)

    if args.command == "models":
        # List available models
        models = client.list_available_models()
        print("Available models:")
        for model in models:
            print(f"  - {model['name']} (ID: {model['id']})")
            # Convert capabilities to list of strings for safe joining
            capabilities = cast(list[str], model["capabilities"])
            print(f"    Capabilities: {', '.join(capabilities)}")
            print(f"    Max tokens: {model['max_tokens']}")
            if model.get("knowledge_cutoff"):
                print(f"    Knowledge cutoff: {model['knowledge_cutoff']}")
            if model.get("private_preview"):
                print(
                    "    Note: This model is in private preview. Contact Cerebras for access."
                )

    elif args.command == "sessions":
        # Since we don't have persistent sessions, just print a message
        print("Active sessions can only be tracked within the current process.")
        print("Use the 'chat' command to start a new session.")
        if hasattr(client, "_sessions") and client._sessions:
            print("\nActive sessions in the current process:")
            for session_id, session in client._sessions.items():
                status = "Active" if session["active"] else "Ended"
                message_count = len(session["history"])
                print(
                    f"  - {session_id} ({status}): Model {session['model']}, "
                    f"{message_count} messages"
                )

    elif args.command == "export":
        # Export chat history for a session
        if not hasattr(client, "_sessions") or args.session_id not in client._sessions:
            print(f"Error: Session {args.session_id} not found.")
            sys.exit(1)

        try:
            export_data = client.export_chat_history(args.session_id, args.format)

            if args.output:
                with open(args.output, "w") as f:
                    f.write(export_data)
                print(f"Chat history exported to {args.output}")
            else:
                print(export_data)

        except Exception as e:
            print(f"Error exporting chat history: {str(e)}")
            sys.exit(1)

    elif args.command == "metrics":
        # Show usage metrics for a session
        if not hasattr(client, "_sessions") or args.session_id not in client._sessions:
            print(f"Error: Session {args.session_id} not found.")
            sys.exit(1)

        try:
            metrics = client.get_usage_metrics(args.session_id)
            display_metrics(metrics)

        except Exception as e:
            print(f"Error getting usage metrics: {str(e)}")
            sys.exit(1)

    elif args.command == "summarize":
        # Generate a summary of the conversation
        if not hasattr(client, "_sessions") or args.session_id not in client._sessions:
            print(f"Error: Session {args.session_id} not found.")
            sys.exit(1)

        try:
            print("Generating conversation summary...")
            summary = client.summarize_conversation(args.session_id)

            if args.output:
                with open(args.output, "w") as f:
                    f.write(summary)
                print(f"Summary saved to {args.output}")
            else:
                print("\nSummary:")
                print(format_ai_response(summary))

        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            sys.exit(1)

    elif args.command == "attach":
        # Attach a file to a session
        if not hasattr(client, "_sessions") or args.session_id not in client._sessions:
            print(f"Error: Session {args.session_id} not found.")
            sys.exit(1)

        try:
            # Check if file exists
            if not os.path.exists(args.file_path):
                print(f"Error: File '{args.file_path}' not found.")
                sys.exit(1)

            success = client.attach_file(
                args.session_id, args.file_path, args.description
            )

            if success:
                print(f"File '{args.file_path}' successfully attached to session.")
            else:
                print(f"Failed to attach file '{args.file_path}' to session.")

        except Exception as e:
            print(f"Error attaching file: {str(e)}")
            sys.exit(1)

    elif args.command == "chat":
        # Start or continue a chat session
        session_id = None
        if args.session_id:
            # Try to use existing session
            if (
                not hasattr(client, "_sessions")
                or args.session_id not in client._sessions
            ):
                print(f"Error: Session {args.session_id} not found.")
                sys.exit(1)
            session_id = args.session_id
            selected_model = client._sessions[session_id]["model"]
            print(f"Continuing session {session_id} with model: {selected_model}")
        else:
            # Create new session
            user_id = f"cli_user_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            session_id = client.start_new_session(user_id, model=args.model)
            print(f"Starting chat with model: {args.model}")
            session_info = (
                f"Session ID: {session_id} "
                f"(save this if you want to continue this session later)"
            )
            print(session_info)

        print("\nType 'exit' or 'quit' to end the conversation.")
        print("Type 'help' to see available commands.")

        # Chat loop
        while True:
            try:
                user_input = input("\nYou: ")

                if user_input.lower() in ["exit", "quit"]:
                    break

                elif user_input.lower() == "help":
                    print("\nAvailable commands:")
                    print("  exit, quit - End the conversation")
                    print("  help - Show this help message")
                    print("  model - List available models and their IDs")
                    print("  model <model_id> - Switch to a different model")
                    print("  models - List available models")
                    print("  metrics - Show usage metrics for this session")
                    print("  export - Export the conversation history as JSON")
                    print("  summarize - Generate a summary of the conversation")
                    attach_help = (
                        "  attach <file_path> [description] - "
                        "Attach a file to the conversation"
                    )
                    print(attach_help)
                    continue

                elif user_input.lower() == "models":
                    models = client.list_available_models()
                    print("\nAvailable models:")
                    for model in models:
                        print(f"  - {model['id']}: {model['name']}")
                    continue

                elif user_input.lower() == "export":
                    export_data = client.export_chat_history(session_id, "json")
                    print("\nExport data (JSON format):")
                    print(export_data)
                    continue

                elif user_input.lower() == "metrics":
                    metrics = client.get_usage_metrics(session_id)
                    display_metrics(metrics)
                    continue

                elif user_input.lower() == "summarize":
                    if len(client._sessions[session_id]["history"]) < 2:
                        print("\nNot enough conversation to summarize yet.")
                        continue

                    print("\nGenerating summary...")
                    try:
                        summary = client.summarize_conversation(session_id)
                        print("\nSummary:")
                        print(format_ai_response(summary))
                    except Exception as e:
                        print(f"\nError generating summary: {str(e)}")
                    continue

                elif user_input.lower().startswith("attach "):
                    # Parse the attach command
                    parts = user_input.split(None, 2)
                    if len(parts) < 2:
                        print("\nError: Missing file path")
                        print("Usage: attach <file_path> [description]")
                        continue

                    file_path = parts[1]
                    description = parts[2] if len(parts) > 2 else None

                    # Check if file exists
                    if not os.path.exists(file_path):
                        print(f"\nError: File '{file_path}' not found")
                        continue

                    try:
                        print(f"\nAttaching file '{file_path}'...")
                        success = client.attach_file(session_id, file_path, description)
                        if success:
                            print("File successfully attached")
                        else:
                            print("Failed to attach file")
                    except Exception as e:
                        print(f"\nError attaching file: {str(e)}")
                    continue

                elif user_input.lower().startswith("model "):
                    # Extract model ID from command
                    parts = user_input.split(None, 1)
                    if len(parts) == 1 or not parts[1].strip():
                        # No model ID provided, so display available models
                        models = client.list_available_models()
                        print("\nAvailable models:")
                        for model in models:
                            print(f"  - {model['name']} (ID: {model['id']})")
                            # Convert capabilities to list of strings for safe joining
                            capabilities = cast(list[str], model["capabilities"])
                            print(f"    Capabilities: {', '.join(capabilities)}")
                            print(f"    Max tokens: {model['max_tokens']}")
                            if model.get("knowledge_cutoff"):
                                print(
                                    f"    Knowledge cutoff: {model['knowledge_cutoff']}"
                                )
                            if model.get("private_preview"):
                                print(
                                    "    Note: This model is in private preview. Contact Cerebras for access."
                                )
                        print("\nUsage: model <model_id>")
                    else:
                        # Extract model ID from command
                        new_model_id = parts[1].strip()
                        try:
                            if client.switch_model(session_id, new_model_id):
                                print(f"\nSwitched to model: {new_model_id}")
                            else:
                                print(f"\nFailed to switch to model: {new_model_id}")
                        except ValueError as e:
                            print(f"\nError: {str(e)}")
                    continue

                # Send message to AI
                print("\nAI is thinking...")
                try:
                    response = client.send_message(session_id, user_input)
                    # Get the response text and ensure it's a string for formatting
                    ai_text = cast(str, response["response"])
                    formatted_response = format_ai_response(ai_text)
                    print(f"\nAI: {formatted_response}")
                except Exception as e:
                    print(f"\nError getting response: {str(e)}")

            except KeyboardInterrupt:
                print("\nInterrupted by user.")
                break
            except Exception as e:
                print(f"\nUnexpected error: {str(e)}")

        print("\nChat ended.")
        client.end_session(session_id)


if __name__ == "__main__":
    main()
