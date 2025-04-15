#!/bin/bash
set -e

# Print Ruff version to assist with debugging
echo "Ruff version:"
ruff --version

echo "Running Ruff to fix all issues including line length errors..."
# Run formatter first to address line wrapping
ruff format src/ tests/

# Then run check with --fix to address remaining issues
ruff check src/ tests/ --fix

# Exit with success if ruff check succeeds
exit $? 