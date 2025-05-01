#!/usr/bin/env python3
import argparse
import os
from src.integration.email_analyzer import analyze_emails_for_spam


def main() -> int:
    """Main entry point for email spam analysis application"""
    parser = argparse.ArgumentParser(
        description="Analyze emails for spam probability using AI."
    )

    parser.add_argument(
        "--output",
        "-o",
        default="spam_analysis.csv",
        help="Output CSV file path (default: spam_analysis.csv)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed progress information",
    )

    args = parser.parse_args()

    if args.verbose:
        print("Starting email spam analysis...")

    try:
        results = analyze_emails_for_spam(args.output)

        if args.verbose:
            print(f"Analysis complete. Processed {len(results)} emails.")
            print(f"Results saved to {os.path.abspath(args.output)}")

            # Print summary statistics
            if results:
                high_spam_count = sum(1 for r in results if r["pct_spam"] >= 75)
                med_spam_count = sum(1 for r in results if 25 <= r["pct_spam"] < 75)
                low_spam_count = sum(1 for r in results if r["pct_spam"] < 25)

                print("\nSpam Analysis Summary:")
                print(f"  High probability spam (≥75%): {high_spam_count}")
                print(f"  Medium probability spam (25-74%): {med_spam_count}")
                print(f"  Low probability spam (<25%): {low_spam_count}")

    except Exception as e:
        print(f"Error during email analysis: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
