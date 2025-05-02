import unittest
from unittest.mock import MagicMock
import os
import csv
from src.integration.email_analyzer import analyze_emails_for_spam, EmailAnalyzer, Email

class TestEmailSpamDetection(unittest.TestCase):
    """Tests for email spam detection functionality"""

    def setUp(self) -> None:
        """Set up test environment"""
        # Create test data
        self.test_emails = [
            Email(
                id="1",
                subject="Congratulations! You've won $1,000,000!",
                body="Click here to claim your prize now!",
                sender="unknown@spammer.com",
                date="2023-04-01"
            ),
            Email(
                id="2",
                subject="Team Meeting Agenda",
                body="Here's the agenda for tomorrow's team meeting.",
                sender="manager@company.com",
                date="2023-04-02"
            ),
            Email(
                id="3",
                subject="Limited Time Offer - 90% Off!",
                body="This exclusive offer ends today. Buy now!",
                sender="sales@discount.com",
                date="2023-04-03"
            )
        ]

        # Create test output file with absolute path
        self.test_output = os.path.abspath("test_output.csv")

    def tearDown(self) -> None:
        """Clean up after tests"""
        # Remove test file if it exists
        try:
            if os.path.exists(self.test_output):
                os.remove(self.test_output)
        except (OSError, FileNotFoundError):
            # Ignore errors if file can't be removed
            pass

    def test_analyze_emails_for_spam(self) -> None:
        """Test analyze_emails_for_spam function"""
        # Create mock AI client
        mock_ai = MagicMock()

        # Configure responses
        mock_ai.send_message.side_effect = [
            {"response": "85"},  # High spam probability
            {"response": "15"},  # Low spam probability
            {"response": "75"},  # Medium-high spam probability
        ]

        # Set up mock inbox client
        mock_inbox = MagicMock()
        mock_inbox.get_emails.return_value = self.test_emails

        # Run analysis
        results = analyze_emails_for_spam(
            self.test_output,
            inbox_client=mock_inbox,
            ai_client=mock_ai
        )

        # Verify results
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["pct_spam"], 85.0)
        self.assertEqual(results[1]["pct_spam"], 15.0)
        self.assertEqual(results[2]["pct_spam"], 75.0)

        # Verify CSV was created with correct structure
        self.assertTrue(os.path.exists(self.test_output))

        # Test invalid response handling
        mock_ai.send_message.side_effect = [
            {"response": "not a number"},  # Invalid response
        ]

        # Should default to zero if response is not a valid number
        results = analyze_emails_for_spam(
            self.test_output,
            inbox_client=MagicMock(get_emails=lambda: [self.test_emails[0]]),
            ai_client=mock_ai
        )

        self.assertEqual(results[0]["pct_spam"], 0.0)

    def test_email_analyzer_class(self) -> None:
        """Test EmailAnalyzer class functionality"""
        # Create test emails
        test_email1 = Email(
            id="test1",
            subject="Test Subject 1",
            body="Test Body 1",
            sender="test1@example.com",
            date="2023-05-01"
        )
        test_email2 = Email(
            id="test2",
            subject="Test Subject 2",
            body="Test Body 2",
            sender="test2@example.com",
            date="2023-05-02"
        )

        # Create mock AI client
        mock_ai_client = MagicMock()

        # Configure responses
        mock_ai_client.generate_response.side_effect = [
            {"response": "80"},  # High spam probability
            {"response": "20"},  # Low spam probability
        ]

        # Create mock inbox client
        mock_inbox = MagicMock()
        mock_inbox.get_emails_list.return_value = [
            {
                "id": "test1",
                "subject": "Test Subject 1",
                "body": "Test Body 1",
                "sender": "test1@example.com",
                "date": "2023-05-01"
            },
            {
                "id": "test2",
                "subject": "Test Subject 2",
                "body": "Test Body 2",
                "sender": "test2@example.com",
                "date": "2023-05-02"
            }
        ]

        # Initialize EmailAnalyzer
        analyzer = EmailAnalyzer(mock_ai_client)

        # Test get_emails method
        emails = analyzer.get_emails(mock_inbox)
        self.assertEqual(len(emails), 2)
        self.assertEqual(emails[0].id, "test1")
        self.assertEqual(emails[1].subject, "Test Subject 2")

        # Test analyze_emails_for_spam method
        analyzed_emails = analyzer.analyze_emails_for_spam([test_email1, test_email2])
        self.assertEqual(len(analyzed_emails), 2)
        self.assertEqual(analyzed_emails[0][1], 80.0)  # First email spam score
        self.assertEqual(analyzed_emails[1][1], 20.0)  # Second email spam score

        # Test error handling in analyze_emails_for_spam
        mock_ai_client.generate_response.side_effect = Exception("Test error")
        analyzed_emails = analyzer.analyze_emails_for_spam([test_email1])
        self.assertEqual(analyzed_emails[0][1], 0.0)  # Should default to zero on error

        # Reset mock for further tests
        mock_ai_client.generate_response.side_effect = None
        mock_ai_client.generate_response.return_value = {"response": "75"}

        # Test generate_report method
        test_analyzed_emails = [
            (test_email1, 85.0),
            (test_email2, 20.0)
        ]

        report = analyzer.generate_report(test_analyzed_emails)
        self.assertEqual(report.threshold, 50.0)
        self.assertEqual(report.spam_count, 1)
        self.assertEqual(report.safe_count, 1)

        # Test export_to_csv method
        analyzer.export_to_csv(report, "test_report.csv")
        self.assertTrue(os.path.exists("test_report.csv"))

        # Verify CSV content
        with open("test_report.csv", "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 3)  # Header + 2 data rows
            expected_header = ["Email ID", "Subject", "Spam Score", "Classification"]
            self.assertEqual(rows[0], expected_header)

    def test_mean_method(self) -> None:
        """Test the static mean method"""
        # Test with normal values
        self.assertEqual(EmailAnalyzer.mean([1, 2, 3, 4]), 2.5)

        # Test with empty list
        self.assertEqual(EmailAnalyzer.mean([]), 0.0)

        # Test with single value
        self.assertEqual(EmailAnalyzer.mean([5]), 5.0)

if __name__ == "__main__":
    unittest.main()
