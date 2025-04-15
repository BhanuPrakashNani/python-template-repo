#!/bin/bash
set -e

# Print Ruff version to assist with debugging
echo "Ruff version:"
ruff --version

echo "Running Ruff with line length errors (E501) ignored..."
ruff check src/ tests/ --ignore=E501 --fix

# Exit with success
exit 0 