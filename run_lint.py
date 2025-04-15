#!/usr/bin/env python
"""Run linting checks on the codebase.

This script runs ruff check on the codebase while ignoring E501 line length errors.
"""

import re
import subprocess
import sys


def main():
    """Run the linter, ignoring E501 line length errors."""
    try:
        print("Running linter (ignoring line length errors)...\n")
        
        # Run ruff and capture its output
        result = subprocess.run(
            ["ruff", "check", "src/", "tests/"], 
            capture_output=True,
            text=True,
            check=False
        )
        
        # Filter out E501 errors from the output
        if result.stdout:
            filtered_lines = []
            error_codes = set()
            
            for line in result.stdout.split('\n'):
                # Skip E501 errors and the "Found X errors" summary line
                if "E501" not in line and not line.startswith("Found "):
                    filtered_lines.append(line)
                    
                    # Extract error code if present
                    error_match = re.search(r'([A-Z][0-9]{3})', line)
                    if error_match:
                        error_codes.add(error_match.group(1))
            
            # Print filtered output
            if filtered_lines:
                print('\n'.join(filtered_lines))
                
            if error_codes:
                print(f"\nFound errors of these types: {', '.join(sorted(error_codes))}")
                print("❌ Checks failed. Fix errors to proceed.")
                exit_code = 1
            else:
                print("\n✅ All checks passed! (Ignoring line length errors)")
                exit_code = 0
        else:
            print("✅ All checks passed!")
            exit_code = 0
        
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