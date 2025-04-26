#!/usr/bin/env python3
"""
Manual test script for email spam detection with AI.
This script can be run directly or used as a reference.
"""
import os
import sys
from typing import List
from unittest.mock import MagicMock

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.integration.email_analyzer import Email, EmailAnalyzer


def create_test_emails() -> List[Email]:
    """Create a list of test emails for analysis"""
    return [
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
        Email(
            id="4",
            subject="Weekly Team Meeting Agenda",
            sender="manager@company.com",
            date="2023-04-04",
            body="Hi everyone, Please find attached the agenda for tomorrow's weekly "
                 "team meeting. Let me know if you have any topics to add. "
                 "Best regards, Your Manager",
        ),
    ]


def main() -> None:
    """Run a manual test of email spam detection"""
    # Use mock AI client
    mock_ai = MagicMock()
    mock_ai.generate_response.side_effect = [
        {"response": "95"},  # Very high spam probability
        {"response": "5"},   # Very low spam probability
        {"response": "85"},  # High spam probability
        {"response": "10"},  # Low spam probability
    ]

    # Create analyzer with mock AI
    analyzer = EmailAnalyzer(mock_ai)

    # Analyze test emails
    test_emails = create_test_emails()
    results = analyzer.analyze_emails_for_spam(test_emails)

    # Generate and display report
    report = analyzer.generate_report(results)

    print(f"\nAnalyzed {report.total_emails} emails.")
    print(f"Spam emails: {report.spam_count}")
    print(f"Safe emails: {report.safe_count}")
    print(f"Average spam score: {report.avg_score:.1f}%")
    print("\nDetailed results:")
    print("-" * 50)

    for email, score in results:
        classification = "SPAM" if score >= report.threshold else "SAFE"
        print(f"ID: {email.id}")
        print(f"Subject: {email.subject}")
        print(f"Spam Score: {score:.1f}%")
        print(f"Classification: {classification}")
        print("-" * 50)

    # Export to CSV
    output_file = "test_spam_results.csv"
    analyzer.export_to_csv(report, output_file)
    print(f"\nResults exported to {output_file}")


if __name__ == "__main__":
    main()
