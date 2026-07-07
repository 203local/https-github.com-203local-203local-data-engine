from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.ai_enrichment.config import RESULTS_FOLDER


def latest_results_file():
    files = sorted(RESULTS_FOLDER.glob("*_results.csv"))
    if not files:
        print("No AI results files found.")
        return None
    return files[-1]


def review_suggestions():
    results_file = latest_results_file()
    if results_file is None:
        return

    df = pd.read_csv(results_file, dtype=str)

    suggestions = df[
        df["review_status"].fillna("").str.lower().eq("ai suggested")
    ]

    if suggestions.empty:
        print("No AI suggestions to review.")
        return

    for idx, row in suggestions.iterrows():
        print("=" * 80)
        print("Business:", row.get("post_title", ""))
        print("Town:", row.get("town", ""))
        print("Website:", row.get("website", ""))
        print("-" * 80)
        print("Suggested Description:")
        print(row.get("suggested_post_content", ""))
        print("-" * 80)
        print("SEO Title:")
        print(row.get("suggested_seo_directory_title", ""))
        print("-" * 80)
        print("Meta Description:")
        print(row.get("suggested_seo_meta_description", ""))
        print("-" * 80)
        print("Keywords:")
        print(row.get("suggested_searchable_keywords", ""))
        print("-" * 80)
        print("Confidence:", row.get("confidence", ""))
        print("Notes:", row.get("notes", ""))
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

    print("AI suggestion review complete.")
    print("Results:", results_file)


if __name__ == "__main__":
    review_suggestions()
