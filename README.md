# Cerebras AI Conversation Client

A Python client for interacting with the Cerebras AI API, providing a clean and simple interface for managing AI conversations.

## Features

* **Session Management**: Create, manage, and end conversation sessions
* **Multiple Models**: Support for various Llama models (Llama 4 Scout, Llama 3.1, Llama 3.3)
* **Chat History**: Track and retrieve conversation history
* **Model Switching**: Change models mid-conversation
* **Usage Metrics**: Track token usage and cost estimates
* **Export**: Save conversations to JSON or text formats
* **Summarization**: Generate AI-powered summaries of conversations
* **Command-line Interface**: Interact with the client via a simple CLI

## Table of Contents

* [Installation](#installation)
* [Command Line Interface](#command-line-interface)
* [Python API Usage](#python-api-usage)
* [API Reference](#api-reference)
* [Architecture](#architecture)
* [Models](#models)
* [Configuration](#configuration)
* [Testing](#testing)
* [Troubleshooting](#troubleshooting)
* [Development](#development)
* [Requirements](#requirements)

## Installation

```bash
# Install dependencies
pip install -e .

# Set your API key
export CEREBRAS_API_KEY="your-cerebras-api-key"
# Or create a .env.local file with CEREBRAS_API_KEY="your-key"
```

## Command Line Interface

The client includes a command-line interface for easy interaction:

```bash
# Start a new chat session
python -m src.components.ai_conversation_client.cli chat

# List available models
python -m src.components.ai_conversation_client.cli models

# Show active sessions
python -m src.components.ai_conversation_client.cli sessions

# Export a conversation history
python -m src.components.ai_conversation_client.cli export <session-id> --format json

# Display usage metrics
python -m src.components.ai_conversation_client.cli metrics <session-id>

# Generate a conversation summary
python -m src.components.ai_conversation_client.cli summarize <session-id>
```

During interactive chat, you can use these commands:
* Type `/help` to see available commands
* Type `/exit` or `/quit` to end the chat session
* Type `/model [model_id]` to switch models
* Type `/export` to export the current conversation
* Type `/metrics` to view usage metrics
* Type `/summarize` to generate a conversation summary

### CLI Command Options

**chat**
```bash
python -m src.components.ai_conversation_client.cli chat [--model MODEL] [--session-id SESSION_ID]
```
- `--model`: Specify the model to use (default: llama-4-scout-17b-16e-instruct)
- `--session-id`: Continue a previous session

**export**
```bash
python -m src.components.ai_conversation_client.cli export SESSION_ID [--format {json,text}] [--output OUTPUT]
```
- `--format`: Export format, either "json" or "text" (default: json)
- `--output`: Save to a file instead of printing to console

**summarize**
```bash
python -m src.components.ai_conversation_client.cli summarize SESSION_ID [--output OUTPUT]
```
- `--output`: Save the summary to a file instead of printing to console

## Python API Usage

Here's how to use the client in your Python code:

```python
import os
from src.components.ai_conversation_client import CerebrasClient

# Initialize the client
client = CerebrasClient(api_key=os.environ.get("CEREBRAS_API_KEY"))

# List available models
models = client.list_available_models()
for model in models:
    print(f"- {model['name']} (ID: {model['id']})")

# Start a new session
user_id = "user123"
session_id = client.start_new_session(user_id, model="llama-4-scout-17b-16e-instruct")

# Send messages and get responses
response = client.send_message(session_id, "What are the latest developments in AI?")
print(f"AI: {response['response']}")

# Get chat history
history = client.get_chat_history(session_id)
for msg in history:
    print(f"[{msg['timestamp']}] {msg['sender'].upper()}: {msg['content']}")

# Get usage metrics
metrics = client.get_usage_metrics(session_id)
print(f"Token count: {metrics['token_count']}")
print(f"Cost estimate: ${metrics['cost_estimate']:.6f}")

# Generate summary
summary = client.summarize_conversation(session_id)
print(f"Summary: {summary}")

# Export history
json_export = client.export_chat_history(session_id, "json")

# End session
client.end_session(session_id)
```

### Extended Example: Working with Multiple Sessions

```python
import os
from src.components.ai_conversation_client import CerebrasClient

# Initialize client
client = CerebrasClient()

# Create multiple sessions with different models
session1 = client.start_new_session("user1", model="llama-4-scout-17b-16e-instruct")
session2 = client.start_new_session("user1", model="llama3.1-8b")

# Send the same query to both models for comparison
query = "Explain the differences between transformers and RNNs in natural language processing"

# Get responses from different models
response1 = client.send_message(session1, query)
response2 = client.send_message(session2, query)

print(f"Llama 4 Scout response:\n{response1['response']}\n")
print(f"Llama 3.1 response:\n{response2['response']}\n")

# Compare usage statistics
metrics1 = client.get_usage_metrics(session1)
metrics2 = client.get_usage_metrics(session2)

print("Usage comparison:")
print(f"Llama 4 Scout: {metrics1['token_count']} tokens, ${metrics1['cost_estimate']:.6f}")
print(f"Llama 3.1: {metrics2['token_count']} tokens, ${metrics2['cost_estimate']:.6f}")

# End both sessions
client.end_session(session1)
client.end_session(session2)
```

## API Reference

### CerebrasClient

The main client for interacting with the Cerebras API.

```python
client = CerebrasClient(api_key="your-cerebras-api-key")  # Optional if set in environment
```

**Methods:**

* `list_available_models()`: Get a list of available AI models
  ```python
  models = client.list_available_models()
  # Returns: [{"id": "model-id", "name": "Model Name", "capabilities": [...], "max_tokens": 8192}, ...]
  ```

* `start_new_session(user_id, model=None)`: Create a new conversation session
  ```python
  session_id = client.start_new_session("user_xyz", model="llama-4-scout-17b-16e-instruct")
  # Returns: "session-uuid-string"
  ```

* `end_session(session_id)`: End an active session
  ```python
  success = client.end_session(session_id)
  # Returns: True if successful, False otherwise
  ```

* `send_message(session_id, message)`: Send a message and get AI response
  ```python
  response = client.send_message(session_id, "What is machine learning?")
  # Returns: {"response": "AI response text", "attachments": [], "timestamp": datetime}
  ```

* `get_chat_history(session_id, limit=None)`: Get conversation history
  ```python
  history = client.get_chat_history(session_id, limit=10)  # Get last 10 messages
  # Returns: [{"id": "msg-id", "content": "message text", "sender": "user|assistant", "timestamp": datetime}, ...]
  ```

* `switch_model(session_id, model_id)`: Change the AI model for an active session
  ```python
  success = client.switch_model(session_id, "llama3.1-8b")
  # Returns: True if successful, False otherwise
  ```

* `get_usage_metrics(session_id)`: Get usage statistics (tokens, calls, cost)
  ```python
  metrics = client.get_usage_metrics(session_id)
  # Returns: {"token_count": 256, "api_calls": 3, "cost_estimate": 0.00256}
  ```

* `summarize_conversation(session_id)`: Generate summary of the conversation
  ```python
  summary = client.summarize_conversation(session_id)
  # Returns: "This conversation discussed topics including..."
  ```

* `export_chat_history(session_id, format="json")`: Export a conversation
  ```python
  json_data = client.export_chat_history(session_id, "json")
  # Returns: JSON string of conversation data
  
  text_data = client.export_chat_history(session_id, "text")
  # Returns: Text format of conversation
  ```

## Architecture

The Cerebras AI Conversation Client is built on a clean, extensible architecture:

### Core Components

1. **`AIConversationClient` (api.py)**: Abstract interface defining the contract for AI conversation clients.
   - Defines standard methods all AI clients must implement
   - Provides type hints and method signatures
   - Enables future implementations for other AI providers

2. **`CerebrasClient` (cerebras_client.py)**: Concrete implementation for Cerebras AI API.
   - Handles API authentication and request formatting
   - Manages session state and history
   - Tracks usage metrics
   - Implements conversation functionalities

3. **Command-line Interface (cli.py)**: User-friendly terminal interface.
   - Provides commands for all major functionalities
   - Formats AI responses for terminal display
   - Handles interactive chat sessions

### Design Principles

- **Interface Segregation**: Clean separation between interface and implementation
- **Stateless API**: Each method call is independent and can be used without dependencies
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Type Safety**: Full type annotations for better IDE support and fewer bugs

### Data Flow

1. User interacts via CLI or imports client directly
2. Requests are formatted and sent to Cerebras API
3. Responses are parsed, processed, and stored in conversation history
4. Results are returned to the user in the requested format

## Models

Currently supports the following Cerebras models:

* **Llama 4 Scout** (`llama-4-scout-17b-16e-instruct`): Large model with 8K context window
  - Best for complex reasoning and creative content
  - Knowledge cutoff: August 2024

* **Llama 3.1 8B** (`llama3.1-8b`): Smaller, faster model
  - More efficient for quick responses
  - Good balance of performance and speed
  - Knowledge cutoff: March 2023

* **Llama 3.3 70B** (`llama-3.3-70b`): Larger model with advanced capabilities
  - Highest quality responses
  - Excellent for complex tasks and specialized knowledge
  - Knowledge cutoff: December 2023

* **DeepSeek R1 Distill Llama 70B** (`deepseek-r1-distill-llama-70b`):
  - Private preview model
  - Contact Cerebras for access
  - Knowledge cutoff: December 2023

## Configuration

The client can be configured in several ways:

### API Authentication

1. **Direct initialization**:
   ```python
   client = CerebrasClient(api_key="your-api-key")
   ```

2. **Environment variable**:
   ```bash
   export CEREBRAS_API_KEY="your-api-key"
   ```
   Then:
   ```python
   client = CerebrasClient()  # Reads from environment
   ```

3. **Environment file**:
   Create a `.env.local` file in your project root:
   ```
   CEREBRAS_API_KEY="your-api-key"
   ```
   The client will automatically load this file.

### API Parameters

When sending messages, you can adjust parameters by modifying the `CerebrasClient` implementation:

* `max_tokens`: Maximum tokens to generate (default: 1024)
* Model parameters: Can be extended to support temperature, top_p, etc.

## Testing

The client includes comprehensive unit tests to ensure reliability:

```bash
# Run all tests
pytest src/components/ai_conversation_client/tests/

# Run with coverage
pytest --cov=src.components.ai_conversation_client
```

### Test Components

- **test_cerebras_client.py**: Tests all client methods:
  - Initialization with API key validation
  - Session management (start/end)
  - Message sending and response handling
  - Model listing and switching
  - Chat history retrieval and handling
  - Usage metrics tracking
  - Error conditions and handling

### Mocking Strategy

Tests use `unittest.mock` to simulate API responses without making real API calls:
- `requests.post` is mocked to return predefined responses
- API errors are simulated to test error handling

## Troubleshooting

### Common Issues

**API Key Not Found**
```
Error: CEREBRAS_API_KEY environment variable is required.
```
**Solution**: Set your API key as described in [Configuration](#configuration).

**Model Not Available**
```
ValueError: Model nonexistent-model is not available
```
**Solution**: Use `client.list_available_models()` to check valid model IDs.

**Session Not Found**
```
Error: Session xxx not found.
```
**Solution**: Ensure you're using a valid session ID from an active session. Session IDs are not persistent across program restarts.

**API Request Failed**
```
RuntimeError: Failed to send message to Cerebras API
```
**Solution**: Check your internet connection, API key validity, and Cerebras service status.

### Debugging

For detailed debugging, you can modify the client to print HTTP request details:

```python
# In cerebras_client.py, modify the send_message method:
try:
    print(f"DEBUG: Sending request to {url}")
    print(f"DEBUG: Payload: {payload}")
    response = requests.post(url, headers=self._headers, json=payload)
    print(f"DEBUG: Response status: {response.status_code}")
    # ...
```

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"  # Installs development dependencies

# Set up pre-commit hooks
pre-commit install
```

### Project Structure

```
src/components/ai_conversation_client/
├── __init__.py          # Package exports
├── api.py               # Interface definition
├── cerebras_client.py   # Cerebras implementation
├── cli.py               # Command-line interface
├── example.py           # Example usage
├── py.typed             # Type checking marker
├── pyproject.toml       # Package configuration
└── tests/               # Test directory
    ├── __init__.py
    └── test_cerebras_client.py
```

### Code Style and Linting

The project follows strict type checking with mypy and adheres to PEP 8 style guidelines:

```bash
# Run type checking
mypy src/

# Run linting
flake8 src/
```

## Requirements

* Python 3.8+
* `requests` library for API calls
* Optional development dependencies:
  * pytest (testing)
  * mypy (type checking)
  * flake8 (linting) 