# AI Conversation Client Interface Specification

## Overview
The `AIConversationClient` class provides an abstract interface for interacting with AI conversation services. This document specifies the complete API contract that all implementations must fulfill.

## Class Definition

```python
class AIConversationClient:
    """Interface for interacting with AI conversation services."""
```

## Core Methods

### Initialization
```python
def __init__(self, api_key: str | None = None) -> None
```
**Purpose**: Initialize a new client instance  
**Parameters**:
- `api_key` (str | None): Service authentication key (optional)

---

### Message Handling
```python
def send_message(
    self,
    session_id: str,
    message: str,
    attachments: list[str] | None = None
) -> dict[str, str | list[str] | datetime]
```
**Purpose**: Send message and receive AI response  
**Parameters**:
- `session_id`: Unique conversation identifier
- `message`: User message content
- `attachments`: Files/URLs to include (optional)

**Response Structure**:
```python
{
    "response": "AI reply text",
    "attachments": ["generated_file1.txt"],  # optional
    "timestamp": datetime(2023, 11, 15, 10, 30)
}
```

---

### Session Management
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `start_new_session(user_id: str, model: str \| None)` | `user_id`: User identifier<br>`model`: AI model to use (optional) | `str`: New session ID | Creates new conversation |
| `end_session(session_id: str)` | `session_id`: Session to terminate | `bool`: Success status | Ends active session |

---

### Data Retrieval
```python
def get_chat_history(
    self,
    session_id: str,
    limit: int | None = None
) -> list[dict[str, str | datetime]]
```
**Example Return**:
```python
[
    {
        "id": "msg_123",
        "content": "Hello AI",
        "sender": "user",
        "timestamp": datetime(2023, 11, 15, 10, 25)
    },
    {
        "id": "msg_124", 
        "content": "Hello human",
        "sender": "ai",
        "timestamp": datetime(2023, 11, 15, 10, 26)
    }
]
```

## Advanced Features

### Model Management
```python
def list_available_models() -> list[dict[str, str | list[str] | int]]
```
**Response Example**:
```python
[
    {
        "id": "gpt-4",
        "name": "GPT-4",
        "capabilities": ["chat", "summarization"],
        "max_tokens": 8192
    }
]
```

### File Operations
```python
def attach_file(
    self,
    session_id: str,
    file_path: str,
    description: str | None = None
) -> bool
```
**Usage**:
```python
client.attach_file(
    session_id="sess_123",
    file_path="document.pdf",
    description="Project specifications"
)
```

## Utility Methods

### Analytics
```python
def get_usage_metrics(session_id: str) -> dict[str, int | float]
```
**Metrics Include**:
- Token count
- API call count
- Cost estimate

### Conversation Tools
```python
def summarize_conversation(session_id: str) -> str:
def export_chat_history(session_id: str, format: str = "json") -> str:
```
