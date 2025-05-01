import unittest
import sys
import os
import tempfile
from unittest.mock import patch, MagicMock
from io import StringIO
from src.main import main
from typing import Any


class TestMain(unittest.TestCase):
    """Tests for the main entry point"""

    def setUp(self) -> None:
        """Set up test environment"""
        # Create a temporary output file
        self.temp_output = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
        self.temp_output.close()

        # Save original stdout and stderr
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        # Create captures for stdout and stderr
        self.stdout_capture = StringIO()
        self.stderr_capture = StringIO()

        # Redirect stdout and stderr
        sys.stdout = self.stdout_capture
        sys.stderr = self.stderr_capture

    def tearDown(self) -> None:
        """Clean up after tests"""
        # Restore original stdout and stderr
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

        # Remove temporary files
        if os.path.exists(self.temp_output.name):
            os.remove(self.temp_output.name)

    @patch('src.main.analyze_emails_for_spam')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_verbose(
        self,
        mock_parse_args: Any,
        mock_analyze: Any
    ) -> None:
        """Test main function with verbose flag"""
        # Configure mocks
        mock_parse_args.return_value = MagicMock(
            output=self.temp_output.name,
            verbose=True
        )

        # Mock analyze_emails_for_spam to return test results
        mock_results = [
            {"mail_id": "email1", "pct_spam": 90.0},
            {"mail_id": "email2", "pct_spam": 10.0},
            {"mail_id": "email3", "pct_spam": 60.0}
        ]
        mock_analyze.return_value = mock_results

        # Run main function
        exit_code = main()

        # Verify analyze_emails_for_spam was called with correct args
        mock_analyze.assert_called_once_with(self.temp_output.name)

        # Verify exit code is 0 (success)
        self.assertEqual(exit_code, 0)

        # Verify verbose output was printed
        stdout = self.stdout_capture.getvalue()
        self.assertIn("Starting email spam analysis", stdout)
        self.assertIn("Analysis complete", stdout)
        self.assertIn("Results saved to", stdout)
        self.assertIn("Processed 3 emails", stdout)
        self.assertIn("High probability spam", stdout)

    @patch('src.main.analyze_emails_for_spam')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_without_verbose(
        self,
        mock_parse_args: Any,
        mock_analyze: Any
    ) -> None:
        """Test main function without verbose flag"""
        # Configure mocks
        mock_parse_args.return_value = MagicMock(
            output=self.temp_output.name,
            verbose=False
        )

        # Mock analyze_emails_for_spam to return test results
        mock_analyze.return_value = [
            {"mail_id": "test1", "pct_spam": 85.0},
        ]

        # Run main function
        exit_code = main()

        # Verify analyze_emails_for_spam was called with correct args
        mock_analyze.assert_called_once_with(self.temp_output.name)

        # Verify exit code is 0 (success)
        self.assertEqual(exit_code, 0)

        # Verify no verbose output
        stdout = self.stdout_capture.getvalue()
        self.assertEqual(stdout, "")

    @patch('src.main.analyze_emails_for_spam')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_with_error(
        self,
        mock_parse_args: Any,
        mock_analyze: Any
    ) -> None:
        """Test main function with error condition"""
        # Configure mocks
        mock_parse_args.return_value = MagicMock(
            output=self.temp_output.name,
            verbose=True
        )

        # Mock analyze_emails_for_spam to raise an exception
        mock_analyze.side_effect = Exception("Test error")

        # Run main function - should handle the exception and return error code
        exit_code = main()

        # Verify analyze_emails_for_spam was called
        mock_analyze.assert_called_once()

        # Verify error was reported
        output = self.stdout_capture.getvalue()
        self.assertIn("Error during email analysis", output)

        # Verify exit code is 1 (error)
        self.assertEqual(exit_code, 1)


if __name__ == "__main__":
    unittest.main()
