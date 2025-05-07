"""End-to-end test for the email spam analysis workflow."""

import unittest
import os
import csv

from src.integration.email_analyzer import Email, EmailAnalyzer
from src.components.ai_conversation_client.test_client import TestCerebrasClient
from dotenv import load_dotenv


class TestEmailSpamE2E(unittest.TestCase):
    """End-to-end test for the email spam analysis workflow"""

    def setUp(self) -> None:
        """Setup test environment"""
        # Load API key from .env.local
        load_dotenv('.env.local')

        # Create test emails with varying spam characteristics
        self.test_emails = [
            Email(
                id="1",
                subject="URGENT: Your Account Will Be Suspended",
                sender="security@suspicious-bank.com",
                date="2023-05-01",
                body=(
                    "Your account will be suspended! Click here to verify "
                    "your information now!"
                )
            ),
            Email(
                id="2",
                subject="Weekly Team Meeting Agenda",
                sender="manager@company.com",
                date="2023-05-02",
                body="Here's the agenda for our upcoming team meeting on Friday."
            ),
            Email(
                id="3",
                subject="Congratulations! You've Won a $1000 Gift Card!!!",
                sender="promo@unknown-sender.com",
                date="2023-05-03",
                body=(
                    "You've been selected to receive a $1000 gift card! "
                    "Click to claim now!"
                )
            )
        ]

        # Set up output file
        self.output_file = "e2e_spam_analysis.csv"

        # Create a test client that doesn't make real API calls but simulates behavior
        self.ai_client = TestCerebrasClient()

        # Configure predetermined responses for spam analysis
        # First email (suspicious): high spam probability, phishing category
        # Second email (work related): low spam probability, business category
        # Third email (promotional): high spam probability, marketing category
        self.ai_client.configure_responses([
            {"response": "90"},  # Email 1 spam probability
            {"response": "Phishing"},  # Email 1 category
            {"response": "15"},  # Email 2 spam probability
            {"response": "Business"},  # Email 2 category
            {"response": "85"},  # Email 3 spam probability
            {"response": "Marketing"}  # Email 3 category
        ])

    def tearDown(self) -> None:
        """Clean up after test"""
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_complete_workflow(self) -> None:
        """Test the complete email analysis workflow from fetching emails to CSV.

        Tests the full process of analyzing emails for spam and exporting results.
        """
        # Create analyzer with our test client
        analyzer = EmailAnalyzer(self.ai_client)

        # Override inbox client to return our test emails
        analyzer.inbox_client.get_emails = lambda: self.test_emails

        # Run analysis on test emails
        results = analyzer.analyze_emails()

        # Verify we got results for all emails
        self.assertEqual(len(results), 3, "Should analyze all 3 test emails")

        # Verify fields in results
        for result in results:
            self.assertIn("email_id", result)
            self.assertIn("subject", result)
            self.assertIn("sender", result)
            self.assertIn("spam_probability", result)
            self.assertIn("category", result)
            self.assertIn("timestamp", result)

        # Verify spam probabilities match expected values
        email1 = next(r for r in results if r["email_id"] == "1")
        email2 = next(r for r in results if r["email_id"] == "2")
        email3 = next(r for r in results if r["email_id"] == "3")

        self.assertEqual(email1["spam_probability"], 90)
        self.assertEqual(email1["category"], "Phishing")

        self.assertEqual(email2["spam_probability"], 15)
        self.assertEqual(email2["category"], "Business")

        self.assertEqual(email3["spam_probability"], 85)
        self.assertEqual(email3["category"], "Marketing")

        # Export to CSV
        analyzer.export_results(results, self.output_file)

        # Verify CSV file was created and has correct content
        self.assertTrue(os.path.exists(self.output_file), "CSV file should be created")

        # Read and verify CSV content
        with open(self.output_file, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

            # Check CSV has correct number of rows
            self.assertEqual(len(rows), 3, "CSV should contain 3 rows")

            # Check CSV has required columns
            self.assertIn("email_id", rows[0], "CSV should have email_id column")
            self.assertIn(
                "spam_probability",
                rows[0],
                "CSV should have spam_probability column"
            )
            self.assertIn("category", rows[0], "CSV should have category column")

            # Test passes if all rows have a valid score
            for row in rows:
                score = int(row["spam_probability"])
                self.assertGreaterEqual(score, 0, "Spam score should be non-negative")
                self.assertLessEqual(score, 100, "Spam score should be at most 100")

        # Use analyzer's session ID which was created during analyze_emails()
        self.assertIsNotNone(analyzer.session_id, "Session ID should be created")

        # Test summary functionality
        summary = self.ai_client.summarize_conversation(analyzer.session_id)
        self.assertIsInstance(summary, str, "Summary should be a string")


if __name__ == "__main__":
    unittest.main()
