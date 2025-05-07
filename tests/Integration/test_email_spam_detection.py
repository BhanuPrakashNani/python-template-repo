"""Integration tests for the email spam detection module."""

import os
from unittest import TestCase

from dotenv import load_dotenv

from src.integration.email_analyzer import Email, EmailAnalyzer
from src.components.ai_conversation_client.factory import AIClientFactory
from src.components.ai_conversation_client.test_client import TestCerebrasClient


class TestEmailSpamDetection(TestCase):
    """Test suite for email spam detection integration."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        # Load environment variables
        dotenv_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            ".env.local"
        )
        load_dotenv(dotenv_path)

        # Get API key if available for real API tests
        api_key = os.environ.get("CEREBRAS_API_KEY", "").strip()
        print(f"DEBUG: API key length: {len(api_key)}")
        if api_key:
            print(f"DEBUG: API key first 5 chars: {api_key[:5]}")

        # Create test emails
        self.test_emails = [
            Email(
                id="1",
                subject="Congratulations! You've won a million dollars!",
                sender="unknown@spammer.com",
                date="2023-04-01",
                body="Click here to claim your prize! Limited time offer!"
            ),
            Email(
                id="2",
                subject="Team Meeting Notes",
                sender="boss@company.com",
                date="2023-04-02",
                body="Here are the notes from yesterday's team meeting. Please review."
            ),
            Email(
                id="3",
                subject="Urgent: Your Account Will Be Suspended",
                sender="security@suspicious-bank.com",
                date="2023-04-03",
                body="Your account will be suspended! Click here to verify now!"
            ),
        ]

        # Set up test output file - use absolute path to current directory
        # In CI environment, use a path that is definitely writable
        if os.environ.get("CI"):
            # Use /tmp directory in CI which is guaranteed to be writable
            self.test_output = "/tmp/test_spam_results.csv"
        else:
            # Use current directory for local testing
            current_dir = os.getcwd()
            self.test_output = os.path.join(current_dir, "test_spam_results.csv")

        print(f"DEBUG: Set test output to absolute path: {self.test_output}")

        # Make sure output directory exists
        os.makedirs(os.path.dirname(self.test_output) or '.', exist_ok=True)

        # Create a test client instead of mocking
        self.ai_client = TestCerebrasClient()

        # Configure test responses for spam analysis
        self.ai_client.configure_responses([
            {"response": "95"},  # Email 1 spam probability (high)
            {"response": "Marketing"},  # Email 1 category
            {"response": "10"},  # Email 2 spam probability (low)
            {"response": "Business"},  # Email 2 category
            {"response": "90"},  # Email 3 spam probability (high)
            {"response": "Phishing"},  # Email 3 category
        ])

        # Register the test client with the factory
        AIClientFactory.register_client("test", TestCerebrasClient)

    def tearDown(self) -> None:
        """Clean up after tests."""
        # Remove test output file if it exists
        if os.path.exists(self.test_output):
            os.remove(self.test_output)

    def test_analyze_emails(self) -> None:
        """Test analyzing emails for spam"""
        # Create analyzer with the test client
        analyzer = EmailAnalyzer(self.ai_client)

        # Override the inbox_client to return our test emails
        analyzer.inbox_client.get_emails = lambda: self.test_emails

        # Run analysis
        print("DEBUG: Starting email analysis")
        results = analyzer.analyze_emails()
        print(f"DEBUG: Analysis results: {results}")

        # Verify results
        self.assertEqual(len(results), 3)

        # Verify each result has expected structure
        for result in results:
            print(
                f"DEBUG: Email {result['email_id']} "
                f"has score {result['spam_probability']}"
            )
            self.assertIn('email_id', result)
            self.assertIn('spam_probability', result)
            self.assertIn('category', result)

            # Verify spam probability is an integer between 0 and 100
            spam_score = result['spam_probability']
            self.assertGreaterEqual(spam_score, 0)
            self.assertLessEqual(spam_score, 100)

        # Export to CSV
        analyzer.export_results(results, self.test_output)

        # Verify CSV was created with correct structure
        self.assertTrue(os.path.exists(self.test_output))
        with open(self.test_output, 'r') as f:
            content = f.read()
            print(f"DEBUG: CSV content: {content}")
            self.assertIn("email_id", content)
            self.assertIn("spam_probability", content)
            self.assertIn("category", content)

    def test_analyze_single_email(self) -> None:
        """Test analyzing a single email"""
        # Create a test email
        test_email = Email(
            id="test1",
            subject="Free Gift Card!",
            sender="promo@example.com",
            date="2023-04-01",
            body="Claim your free gift card now!"
        )

        # Configure test responses
        self.ai_client.configure_responses([
            {"response": "85"},  # Spam probability
            {"response": "Marketing"},  # Category
        ])

        # Create analyzer with test client
        analyzer = EmailAnalyzer(self.ai_client)

        # Analyze single email
        result = analyzer.analyze_single_email(test_email)

        # Verify result structure and content
        self.assertIn('email_id', result)
        self.assertEqual(result['email_id'], "test1")
        self.assertIn('subject', result)
        self.assertEqual(result['subject'], "Free Gift Card!")
        self.assertIn('sender', result)
        self.assertEqual(result['sender'], "promo@example.com")
        self.assertIn('spam_probability', result)
        self.assertEqual(result['spam_probability'], 85)
        self.assertIn('category', result)
        self.assertEqual(result['category'], "Marketing")
        self.assertIn('timestamp', result)

    def test_export_results(self) -> None:
        """Test CSV export functionality"""
        # Add debugging for CI environment
        print(f"DEBUG: Running in CI: {bool(os.environ.get('CI'))}")
        print(f"DEBUG: Current directory: {os.getcwd()}")
        print(f"DEBUG: Directory contents: {os.listdir('.')}")
        print(f"DEBUG: Test output file: {self.test_output}")
        print(f"DEBUG: Test output is absolute path: {os.path.isabs(self.test_output)}")

        # Configure test responses
        self.ai_client.configure_responses([
            {"response": "95"},  # Email 1 spam probability
            {"response": "Marketing"},  # Email 1 category
            {"response": "10"},  # Email 2 spam probability
            {"response": "Business"},  # Email 2 category
            {"response": "90"},  # Email 3 spam probability
            {"response": "Phishing"},  # Email 3 category
        ])

        # Create analyzer with test client
        analyzer = EmailAnalyzer(self.ai_client)

        # Override the inbox_client to return our test emails
        analyzer.inbox_client.get_emails = lambda: self.test_emails

        # Run analysis
        results = analyzer.analyze_emails()
        print(f"DEBUG: Analysis results count: {len(results)}")

        # Try creating a file manually first to check permissions
        try:
            test_file = "test_perm_check.txt"
            with open(test_file, 'w') as f:
                f.write("Testing permissions")
            if os.path.exists(test_file):
                print(f"DEBUG: Permission test file created successfully: {test_file}")
                os.remove(test_file)
            else:
                print("DEBUG: Failed to create permission test file")
        except Exception as e:
            print(f"DEBUG: Permission test file error: {str(e)}")

        # Export to CSV
        print(
            f"DEBUG: About to call export_results with output file: {self.test_output}"
        )
        analyzer.export_results(results, self.test_output)

        # Check if file exists
        file_exists = os.path.exists(self.test_output)
        print(f"DEBUG: File exists check: {file_exists}")
        if not file_exists:
            print(f"DEBUG: Directory after export: {os.listdir('.')}")

        # Verify file was created and has correct structure
        self.assertTrue(
            os.path.exists(self.test_output),
            f"Output file {self.test_output} does not exist"
        )

        # Only try to open the file if it exists
        if file_exists:
            with open(self.test_output, 'r') as f:
                content = f.read()
                print(f"DEBUG: CSV content: {content}")
                self.assertIn("email_id", content)
                self.assertIn("spam_probability", content)
                self.assertIn("category", content)
