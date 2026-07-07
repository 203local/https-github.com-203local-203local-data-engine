from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.email_discovery.config import RESULTS_FOLDER


def latest_results_file():
    files = sorted(RESULTS_FOLDER.glob("*_interactive_results.csv"))
    if not files:
        print("No email results files found.")
        return None
    return files[-1]


def review_suggestions():
    results_file = latest_results_file()
    if results_file is None:
        return

    df = pd.read_csv(results_file, dtype=str)

    suggestions = df[
        df["review_status"].fillna("").str.lower().eq("auto email suggested")
    ]

    if suggestions.empty:
        print("No auto email suggestions to review.")
        return

    for idx, row in suggestions.iterrows():
        print("=" * 70)
        print("Business:", row.get("post_title", ""))
        print("Town:", row.get("town", ""))
        print("Website:", row.get("website", ""))
        print("Suggested email:", row.get("suggested_email", ""))
        print("Source:", row.get("source_url", ""))
        print("Confidence:", row.get("confidence", ""))
        print("Notes:", row.get("notes", ""))
        print("=" * 70)

        choice = input("[A] Approve  [R] Reject  [S] Skip  [Q] Quit: ").strip().lower()

        if choice == "a":
            df.at[idx, "review_status"] = "Email Found"
            df.at[idx, "ready_to_merge"] = "Yes"
            print("✓ Approved")
        elif choice == "r":
            df.at[idx, "review_status"] = "Rejected Auto Suggestion"
            df.at[idx, "ready_to_merge"] = "No"
            print("✓ Rejected")
        elif choice == "s":
            print("Skipped for now")
        elif choice == "q":
            df.to_csv(results_file, index=False)
            print("Progress saved.")
            return
        else:
            print("Invalid option; skipped.")

        df.to_csv(results_file, index=False)

    print("Suggestion review complete.")
    print("Results:", results_file)


if __name__ == "__main__":
    review_suggestions()
