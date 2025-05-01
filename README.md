# Email Spam Detection - Component Integration Project

This project demonstrates the integration of an AI Conversation Client with a Mail Client component to analyze emails for spam probability. This was completed as part of the HW4 assignment to integrate components across teams.

## Project Overview

The application performs the following functions:
- Retrieves emails from a mailbox using a mail client component
- Analyzes each email with an AI conversation client to determine spam probability
- Outputs results to a CSV file with email ID and spam probability percentage

## Components

### Core Components

1. **AI Conversation Client**
   - Provides an interface to AI models for text analysis
   - Implemented as a Python module with a clean API
   - Supports multiple AI backends including Cerebras

2. **Mail Client** (External)
   - Integrated from another team (Davina0316)
   - Provides access to email data
   - Integrated as a Git submodule

### Integration

The integration between these components is handled by the `email_analyzer.py` module, which:
- Retrieves emails using the mail client
- Processes each email with a specialized prompt for spam detection
- Extracts numerical spam probability from AI responses
- Formats and outputs results to CSV

## Installation

### Prerequisites
- Python 3.8+ (recommended)
- Git
- pip or uv for package management

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/BhanuPrakashNani/python-template-repo.git
   cd python-template-repo
   ```

2. Check out the project branch:
   ```bash
   git checkout hw4-step1
   git submodule update --init --recursive
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Unix/MacOS:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   # Using pip:
   pip install -e .
   
   # Or using uv (faster):
   uv pip install -e .
   ```

5. Configure API key:
   Create a `.env.local` file with your Cerebras API key:
   ```
   CEREBRAS_API_KEY="your-api-key"
   ```

## Usage

Run the spam analysis with:

```bash
python -m src.main --output results.csv --verbose
```

Options:
- `--output`: Specify the output CSV file path (default: spam_analysis.csv)
- `--verbose`: Print detailed progress information

## Output

The program generates a CSV file with the following columns:
- `mail_id`: Unique identifier for each email
- `pct_spam`: Percentage probability that the email is spam (0-100)

Example output:
```
mail_id,pct_spam
email1,95.0
email2,5.0
```

## Testing

The project includes comprehensive testing at multiple levels:

### Unit Tests

```bash
python -m pytest tests/unit/
```

These tests verify individual components in isolation, including:
- `CerebrasClient` functionality
- Email parsing and formatting utilities
- Spam analysis algorithms

### Integration Tests

```bash
python -m pytest tests/integration/
```

These tests verify that:
- The mail client and AI client components interact correctly
- Emails are correctly processed and analyzed
- Results are properly formatted and saved to CSV

### End-to-End Tests

```bash
python -m pytest tests/end_to_end/
```

These tests verify the complete workflow from email retrieval to CSV generation with realistic test data.

### Running All Tests

To run all tests with coverage reporting:

```bash
python -m pytest --cov=src
```

## Project Structure

```
├── src/
│   ├── components/           # AI conversation client
│   │   └── cerebras_client.py
│   ├── integration/          # Integration code
│   │   └── email_analyzer.py # Core integration module
│   └── main.py               # CLI entrypoint
├── tests/
│   ├── unit/                 # Unit tests
│   │   └── test_cerebras_client.py
│   ├── integration/          # Integration tests
│   │   └── test_email_spam_detection.py
│   └── end_to_end/           # End-to-end tests
│       └── test_email_spam_e2e.py
├── external/
│   └── mail-client/          # External mail client (submodule)
└── .env.local                # Environment variables (API keys)
```

## Dependencies

- **Core Dependencies:**
  - Python 3.8+
  - Mail client component (external)
  - Cerebras AI API

- **Testing Dependencies:**
  - pytest
  - pytest-cov
  - unittest.mock

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
