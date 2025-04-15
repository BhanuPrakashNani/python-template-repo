#!/usr/bin/env python
"""Run linting checks on the codebase.

This script runs ruff check on the codebase while ignoring E501 line length errors.
"""

import subprocess
import sys


def main():
    """Run the linter, ignoring E501 line length errors."""
    print("Running linter (ignoring line length errors)...\n")
    
    # Run ruff with E501 errors explicitly ignored
    try:
        result = subprocess.run(
            ["ruff", "check", "src/", "tests/", "--ignore=E501"],
            check=False
        )
        
        if result.returncode == 0:
            print("\n✅ All checks passed! (Ignoring line length errors)")
            exit_code = 0
        else:
            print("\n❌ Checks failed. Fix errors to proceed.")
            exit_code = 1
        
        # Also run ruff format to check formatting
        print("\nChecking code formatting...")
        format_result = subprocess.run(
            ["ruff", "format", "--check", "src/", "tests/"],
            capture_output=True,
            text=True,
            check=False
        )
        
        if format_result.returncode != 0:
            print("❌ Formatting checks failed.")
            print(format_result.stdout)
            print("Run 'ruff format src/ tests/' to fix formatting issues.")
            exit_code = 1
        else:
            print("✅ Formatting checks passed!")
            
        sys.exit(exit_code)
    except Exception as e:
        print(f"Error running linter: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 