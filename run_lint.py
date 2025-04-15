#!/usr/bin/env python
"""Run linting checks on the codebase.

This script runs ruff check and ruff format to fix all linting issues including line length.
"""

import subprocess
import sys


def main():
    """Run the linter and formatter to fix line length issues."""
    try:
        # First run ruff format to address line length and formatting
        print("Step 1: Running ruff format to fix formatting issues...")
        format_result = subprocess.run(
            ["ruff", "format", "src/", "tests/"],
            check=False
        )
        
        if format_result.returncode != 0:
            print("❌ Formatting failed. Manual intervention needed.")
            return format_result.returncode
        
        # Then run ruff check with --fix to address any remaining issues
        print("\nStep 2: Running ruff check to fix remaining linting issues...")
        result = subprocess.run(
            ["ruff", "check", "src/", "tests/", "--fix"],
            check=False
        )
        
        # Final verification
        print("\nStep 3: Verifying all issues have been fixed...")
        verify_result = subprocess.run(
            ["ruff", "check", "src/", "tests/"],
            check=False
        )
        
        if verify_result.returncode == 0:
            print("\n✅ All checks passed!")
            return 0
        else:
            print("\n❌ Some issues could not be automatically fixed.")
            print("Please address remaining issues manually.")
            return verify_result.returncode
            
    except Exception as e:
        print(f"Error running linter: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 