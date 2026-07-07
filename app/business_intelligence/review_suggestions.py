from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.business_intelligence.config import RESULTS_FOLDER


def latest_results_file():
    files = sorted(RESULTS_FOLDER.glob("*_results.csv"))
    if not files:
        print("No business intelligence results files found.")
        return None
    return files[-1]


def review_suggestions():
    results_file = latest_results_file()
    if results_file is None:
        return

    df = pd.read_csv(results_file, dtype=str)

    suggestions = df[
        df["review_status"].fillna("").str.lower().eq("business intelligence suggested")
    ]

    if suggestions.empty:
        print("No business intelligence suggestions to review.")
        return

    for idx, row in suggestions.iterrows():
        print("=" * 80)
        print("Business:", row.get("post_title", ""))
        print("Town:", row.get("town", ""))
        print("Website:", row.get("website", ""))
        print("-" * 80)
        print("Current Primary Type:", row.get("primary_business_type", ""))
        print("Suggested Primary Type:", row.get("suggested_primary_business_type", ""))
        print("Suggested Business Types:", row.get("suggested_business_types", ""))
        print("Offerings:", row.get("suggested_offerings_tags", ""))
        print("Services:", row.get("suggested_service_tags", ""))
        print("Amenities:", row.get("suggested_amenities_tags", ""))
        print("Audience:", row.get("suggested_audience_tags", ""))
        print("Ownership:", row.get("suggested_ownership_tags", ""))
        print("Service Model:", row.get("suggested_service_model_tags", ""))
        print("Keywords:", row.get("suggested_searchable_keywords", ""))
        print("-" * 80)
        print("Review Needed:", row.get("suggested_review_needed", ""))
        print("Existing Data Conflict:", row.get("suggested_existing_data_conflict", ""))
        print("Review Reason:", row.get("suggested_review_reason", ""))
        print("Confidence:", row.get("confidence", ""))
        print("Notes:", row.get("suggested_business_intelligence_notes", "") or row.get("notes", ""))
        print("=" * 80)

        choice = input("[A] Approve  [R] Reject  [S] Skip  [Q] Quit: ").strip().lower()

        if choice == "a":
            df.at[idx, "review_status"] = "Approved"
            df.at[idx, "ready_to_merge"] = "Yes"
            print("✓ Approved")
        elif choice == "r":
            df.at[idx, "review_status"] = "Rejected"
            df.at[idx, "ready_to_merge"] = "No"
            print("✓ Rejected")
        elif choice == "s":
            df.at[idx, "review_status"] = "Skipped"
            df.at[idx, "ready_to_merge"] = "No"
            print("✓ Skipped")
        elif choice == "q":
            df.to_csv(results_file, index=False)
            print("Progress saved.")
            return
        else:
            print("Invalid option; skipped.")

        df.to_csv(results_file, index=False)

    print("Business intelligence review complete.")
    print("Results:", results_file)


if __name__ == "__main__":
    review_suggestions()
