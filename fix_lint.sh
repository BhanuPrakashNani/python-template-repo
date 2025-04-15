#!/bin/bash
set -e

# Run ruff format to fix formatting issues and wrap long lines
ruff format src/ tests/

# Run ruff check with fix to address remaining issues
ruff check src/ tests/ --fix

echo "Line length issues fixed!" 