import unittest
import os
import csv
from unittest.mock import MagicMock
from src.integration.email_analyzer import analyze_emails_for_spam


class TestEmailSpamE2E(unittest.TestCase):
    """End-to-end test for the email spam analysis workflow"""

    def setUp(self) -> None:
        """Setup test environment"""
        self.output_file = "e2e_spam_analysis.csv"

        # Create realistic test emails
        self.test_emails = [
            MagicMock(
                id="msg001",
                subject="URGENT: Your Account Has Been Compromised",
                sender="security@bank-secure-alerts.com",
                date="2023-04-10",
                body="Dear Customer, Your account has been compromised. Click here "
                     "immediately to verify your identity and restore access: "
                     "http://suspicious-link.com",
            ),
            MagicMock(
                id="msg002",
                subject="Meeting agenda for tomorrow",
                sender="manager@company.com",
                date="2023-04-11",
                body="Hi team, Please find attached the agenda for tomorrow's "
                     "quarterly planning meeting. Let me know if you have any "
                     "questions. Regards, Manager",
            ),
            MagicMock(
                id="msg003",
                subject="WINNER NOTIFICATION!!!",
                sender="lottery@international-winners.org",
                date="2023-04-12",
                body="CONGRATULATIONS! You have been selected as a winner in our "
                     "international lottery. You won $5,000,000. To claim your prize, "
                     "send your bank details and processing fee of $100.",
            ),
        ]

    def tearDown(self) -> None:
        """Clean up after test"""
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_complete_workflow(self) -> None:
        """Test the complete email analysis workflow from fetching emails to CSV
        generation"""
        # Set up mailbox client mock
        mock_inbox = MagicMock()
        mock_inbox.get_emails.return_value = [
            MagicMock(
                id="msg001",
                subject="Your Account Has Been Compromised",
                sender="security@suspicious.com",
                date="2023-04-10",
                body="Your account has been compromised. Click here immediately to "
                     "verify your identity and restore access: http://suspicious-link.com"
            ),
            MagicMock(
                id="msg002",
                subject="Team Meeting",
                sender="manager@company.com",
                date="2023-04-11",
                body="Please find attached the agenda for tomorrow's quarterly "
                     "planning meeting. Let me know if you have any questions. "
                     "Regards, Manager"
            ),
            MagicMock(
                id="msg003",
                subject="You Won the Lottery!",
                sender="lottery@winner.com",
                date="2023-04-12",
                body="Congratulations! You have been selected as the winner of our "
                     "international lottery. You won $5,000,000. To claim your prize, "
                     "send your bank details and processing fee of $100."
            ),
        ]

        # Set up AI client with more realistic responses
        mock_ai = MagicMock()
        mock_ai.start_new_session.return_value = "e2e_session"

        # Define AI responses for different email types
        def ai_response_side_effect(
            session_id: str,
            prompt: str
        ) -> dict[str, str]:
            if "Your Account Has Been Compromised" in prompt:
                return {"response": "85"}  # High spam probability
            elif "Team Meeting" in prompt:
                return {"response": "12"}  # Low spam probability
            elif "Won the Lottery" in prompt:
                return {"response": "98"}  # Very high spam probability
            return {"response": "50"}  # Default

        mock_ai.send_message.side_effect = ai_response_side_effect

        # Execute the analysis workflow with our mock objects
        results = analyze_emails_for_spam(
            self.output_file, inbox_client=mock_inbox, ai_client=mock_ai
        )

        # Verify the workflow executed correctly
        self.assertEqual(len(results), 3)

        # Verify CSV file was created and has correct content
        self.assertTrue(os.path.exists(self.output_file))

        # Read and verify CSV content
        with open(self.output_file, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)

            # Check CSV has correct number of rows
            self.assertEqual(len(rows), 3)

            # Check CSV has required columns
            self.assertIn("mail_id", rows[0])
            self.assertIn("pct_spam", rows[0])

            # Verify specific values
            email_results = {row["mail_id"]: float(row["pct_spam"]) for row in rows}
            self.assertAlmostEqual(email_results["msg001"], 85.0)
            self.assertAlmostEqual(email_results["msg002"], 12.0)
            self.assertAlmostEqual(email_results["msg003"], 98.0)

            # Verify business logic - spam emails have higher probabilities
            self.assertGreater(email_results["msg001"], email_results["msg002"])
            self.assertGreater(email_results["msg003"], email_results["msg001"])


if __name__ == "__main__":
    unittest.main()
