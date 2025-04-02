# Python Template Repository

This repository serves as a **template** for Python projects. It includes a pre-configured setup for build management, unit testing, continuous integration, static analysis, code style adherence, and component specification. The repository is designed to be fully functional and follows best practices for software development.

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/BhanuPrakashNani/python-template-repo/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/BhanuPrakashNani/python-template-repo/tree/main)

---

## Features
- **Testing Framework**: [Nose2](https://nose2.readthedocs.io/) for unit, integration, and end-to-end testing.
- This repository can also be used with [pytest](https://docs.pytest.org/), a popular testing framework. However, for extra credit, we have disabled `pytest` and are currently using `nose2` as an alternative.
- **Dependency Management**: [UV](https://github.com/astral-sh/uv) for fast and efficient dependency management.
- **Testing Framework**: [pytest](https://docs.pytest.org/) for unit, integration, and end-to-end testing.
- **Code Formatting**: [Ruff](https://beta.ruff.rs/docs/) for linting and formatting.
- **Static Analysis**: [Mypy](https://mypy-lang.org/) and Ruff for type checking and static analysis.
- **Code Coverage**: [Coverage.py](https://coverage.readthedocs.io/) for measuring test coverage.
- **CI/CD**: [CircleCI](https://circleci.com/) for continuous integration and deployment.
- **Pre-configured Templates**: Issue and pull request templates for standardized contributions.
- **Components**: Includes three components (`Calculator`, `Logger`, and `Notifier`) with unit, integration, and end-to-end tests.

---

## Getting Started

### Prerequisites
- Python 3.11 or higher.
- [Git](https://git-scm.com/) for version control.
- A [CircleCI](https://circleci.com/) account for CI/CD (optional).

---

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/python-template-repo.git
   cd python-template-repo
   ```

2. Install dependencies using UV:
   ```bash
   uv pip install -e ".[dev]"
   ```

---

### Running Tests
1. Run unit tests:
   ```bash
   pytest src/components/calculator/tests/test_calculator.py
   ```

2. Run integration tests:
   ```bash
   nose2 tests/Integration
   ```

3. Run end-to-end tests:
   ```bash
   nose2 tests/EndToEnd
   ```

4. Generate a coverage report:
   ```bash
   nose2 --with-coverage
   ```

---

### Continuous Integration (CI) Status
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/BhanuPrakashNani/python-template-repo/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/BhanuPrakashNani/python-template-repo/tree/main)

---

## Components
For detailed documentation on the components (`Calculator`, `Logger`, and `Notifier`), see [component.md](component.md).

---

## Repository Structure
```
python-template-repo/
├── .circleci
│   └── config.yml
├── .github
│   ├── ISSUE_TEMPLATE
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
├── .gitignore
├── .pre-commit-config.yaml
├── .pytest_cache
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   ├── README.md
│   └── v
│       └── cache
│           ├── lastfailed
│           ├── nodeids
│           └── stepwise
├── LICENSE
├── README.md
├── components.md
├── example.py
├── mypy.ini
├── nose2.cfg
├── pyproject.toml
├── python_template_repo.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   └── top_level.txt
├── src
│   ├── __init__.py
│   └── components
│       ├── __init__.py
│       ├── calculator
│       │   ├── __init__.py
│       │   └── pyproject.toml
│       ├── logger
│       │   ├── __init__.py
│       │   └── pyproject.toml
│       └── notifier
│           ├── __init__.py
│           └── pyproject.toml
├── test-results
│   └── junit.xml
└── tests
    ├── EndToEnd
    │   ├── __init__.py
    │   └── test_e2e.py
    └── Integration
        ├── __init__.py
        ├── test_calculator_logger_integration.py
        └── test_logger_notifier_integration.py

```

---

## Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request and follow the template.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- [Nose2](https://nose2.readthedocs.io/) for testing.
- [Ruff](https://beta.ruff.rs/docs/) for linting and formatting.
- [CircleCI](https://circleci.com/) for CI/CD.

---

## Contact
For questions or feedback, please open an issue or contact the maintainers.
