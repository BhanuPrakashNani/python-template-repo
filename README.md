
# Python AI Conversation Framework

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/BhanuPrakashNani/python-template-repo/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/BhanuPrakashNani/python-template-repo/tree/main)

A template for AI conversation services with built-in quality enforcement and CI/CD pipeline.

## Features

### Core Components
- **AI Conversation Interface**: Standardized client interface for multiple AI providers
- **Testing Framework**: [pytest](https://docs.pytest.org/) with 100% coverage enforcement
- **Dependency Management**: [UV](https://github.com/astral-sh/uv) for fast installations
- **Code Quality**: 
  - [Ruff](https://beta.ruff.rs/docs/) linting/formatting
  - [Mypy](https://mypy-lang.org/) static type checking
- **CI/CD**: [CircleCI](https://circleci.com/) with parallel test execution
- **Pre-configured Templates**: Standardized issue and PR templates

### AI Conversation Client Interface
```python
from components.ai_conversation_client import AIConversationClient

class MyAIClient(AIConversationClient):
    # Implements 11 required methods:
    # - send_message() 
    # - get_chat_history()
    # - manage_sessions()
    # - model_operations()
    # - file_attachments()
    # - usage_analytics()
```

**Key Capabilities**:
- Multi-model support
- Session persistence
- File attachments
- Usage metrics
- Conversation summarization

## Project Scope

### In Scope (MVP)
✅ **Core Interface**  
- Strictly typed abstract base class
- Complete test coverage
- Documentation generation

✅ **Quality Enforcement**  
- Static type checking
- Linting/formatting
- 100% test coverage requirement

✅ **CI Pipeline**  
- Parallel test execution
- Automated reporting
- Dependency scanning

✅ **Documentation**  
- Interface specification
- Usage examples
- Contribution guidelines

### Out of Scope
❌ **Concrete Implementations**  
- Provider-specific clients (OpenAI, Anthropic, etc.)
- Authentication handlers
- Rate limiting

❌ **Advanced Features**  
- Streaming responses
- Fine-grained permissions
- Multi-modal attachments

❌ **Deployment**  
- Containerization
- Cloud deployment scripts
- Scaling configuration

## Getting Started

### Prerequisites
- Python 3.11+
- [UV](https://github.com/astral-sh/uv) (`pip install uv`)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/BhanuPrakashNani/python-template-repo.git
   cd python-template-repo
   ```

2. Install dependencies using UV:
   ```bash
   uv pip install -e ".[dev]"
   ```

### Running Tests
```bash
# Unit tests
pytest src/components/ai_conversation_client/tests/

# With coverage
pytest --cov=src --cov-report=html
```

## Repository Structure
```
python-template-repo/
├── src/
│   └── components/
│       ├── ai_conversation_client/
│       │   ├── api.py              # Interface definition
│       │   └── tests/              # Contract tests
├── docs/
│   └── interface.md                # API specification
└── .circleci/                      # CI pipeline
```

## Contributing

1. Fork the repository
2. Implement new AI providers (see `interface.md`)
3. Maintain 100% test coverage
4. Submit PR with:
   - Type checking passing
   - Lint/formatting clean
   - Updated documentation
