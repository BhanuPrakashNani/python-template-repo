# Python AI Conversation Framework

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/BhanuPrakashNani/python-template-repo/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/BhanuPrakashNani/python-template-repo/tree/main)

A modern, test-driven Python framework for building AI conversation clients with built-in quality enforcement and CI/CD integration.

---

## 🚀 Features

### Core Components
- **AI Client Interface**: Abstract base class (`AIConversationClientInterface`) defining the contract for AI conversation clients
- **Protocol Support**: Dependency-injectable `APIClientProtocol` for backend independence
- **Testing Framework**: [pytest](https://docs.pytest.org/) with 100% coverage requirement
- **Dependency Management**: [UV](https://github.com/astral-sh/uv) for ultra-fast installs
- **Code Quality**:
  - [Ruff](https://beta.ruff.rs/docs/) for linting and formatting
  - [Mypy](https://mypy-lang.org/) for static type checking
- **CI/CD**: [CircleCI](https://circleci.com/) with parallel test execution and coverage reporting
- **Developer Experience**:
  - Preconfigured issue and PR templates
  - Fast local dev setup with `uv`

---

## 🧩 Interface Design

### `AIConversationClientInterface`
An abstract base class that defines the following core responsibilities:

- `send_message()`
- `get_chat_history()`
- `start_new_session()`
- `end_session()`
- `list_available_models()`
- `switch_model()`
- `attach_file()`
- `get_usage_metrics()`
- `summarize_conversation()`
- `export_chat_history()`

### `APIClientProtocol`
Defines the injectable backend interface that your AI client implementation depends on. Supports full mockability and unit test separation.

---

## 🧪 Testing

### Interface Contract Testing
```bash
pytest src/components/ai_conversation_client/tests/
```

### With Coverage Report
```bash
pytest --cov=src --cov-report=html
```

All tests are written against `AIConversationClientInterface` using `create_autospec()` and `cast()` to ensure type-safety and contract compliance.

---

## 📦 Getting Started

### Prerequisites
- Python 3.11+
- [UV](https://github.com/astral-sh/uv)

### Installation
```bash
git clone https://github.com/BhanuPrakashNani/python-template-repo.git
cd python-template-repo
uv pip install -e ".[dev]"
```

---

## 📁 Repository Structure

```
python-template-repo/
├── src/
│   └── components/
│       └── ai_conversation_client/
│           ├── api.py              # Interface implementation (incomplete)
│           ├── interface.py        # Abstract base class + protocol
│           └── tests/              # Contract-driven unit tests
├── docs/
│   └── interface.md                # API specification and extension guidelines
└── .circleci/                      # CircleCI pipeline config
```

---

## 📌 Project Scope

### ✅ In Scope (MVP)
- Interface-first architecture
- Full typing + linting enforcement
- Complete unit tests and mock interface testing
- CircleCI with parallel execution

### ❌ Out of Scope
- Real backend integrations (e.g. OpenAI, Claude, etc.)
- Streaming support or multimodal APIs
- Deployment (Docker, k8s, etc.)

---

## 🤝 Contributing

1. Fork the repository
2. Implement a new AI provider client using `APIClientProtocol`
3. Ensure full test coverage and interface compliance
4. Submit a pull request with:
   - ✅ Type checks passing (`uv run mypy`)
   - ✅ Linting clean (`uv run ruff check src/`)
   - ✅ 100% unit test coverage (`pytest --cov`)
   - ✅ Updated documentation in `interface.md`

---

## 🧠 Example Usage

```python
from components.ai_conversation_client.api import AIConversationClient
from components.ai_conversation_client.interface import APIClientProtocol

class MyBackendClient(APIClientProtocol):
    # implement all protocol methods...

client = AIConversationClient(api_client=MyBackendClient())
session_id = client.start_new_session("user123")
response = client.send_message(session_id, "Hello world!")
```

---
