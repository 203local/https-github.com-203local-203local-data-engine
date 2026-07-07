from pathlib import Path
import sys
import pandas as pd
import webbrowser
from urllib.parse import quote_plus

# -------------------------------------------------------------------
# Project setup
# -------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.jobs.website_discovery.discovery_config import (
    DEFAULT_BATCH_FILE,
    RESULTS_FOLDER,
)

OUTPUT_FILE = RESULTS_FOLDER / "website_batch_0001_interactive_results.csv"


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def search_url(name, town):
    query = f"{name} {town} CT official website"
    return "https://www.google.com/search?q=" + quote_plus(query)


# -------------------------------------------------------------------
# Main interactive workflow
# -------------------------------------------------------------------

def run():
    RESULTS_FOLDER.mkdir(parents=True, exist_ok=True)

    # Resume previous work if it exists
    if OUTPUT_FILE.exists():
        print("Resuming previous session...")
        df = pd.read_csv(OUTPUT_FILE)
    else:
        print("Starting new batch...")
        df = pd.read_csv(DEFAULT_BATCH_FILE)

    for idx, row in df.iterrows():

        status = str(row.get("review_status", "")).strip().lower()

        if status in (
            "website found",
            "skipped",
            "no website found",
        ):
            continue

        name = row.get("post_title", "")
        town = row.get("town", "")
        phone = row.get("phone", "")

        print()
        print("=" * 60)
        print(f"{idx + 1}/{len(df)}")
        print(f"Business: {name}")
        print(f"Town: {town}")
        print(f"Phone: {phone}")
        print("=" * 60)

        while True:

            print("[G] Open Google Search")
            print("[S] Save Website")
            print("[K] Skip")
            print("[Q] Quit")

            choice = input("Choose: ").strip().lower()

            if choice == "g":
                webbrowser.open(search_url(name, town))

            elif choice == "s":

                website = input("Website URL: ").strip()

                source = (
                    input("Source URL (Enter for same): ").strip()
                    or website
                )

                confidence = (
                    input("Confidence (High/Medium/Low): ").strip()
                    or "High"
                )

                df.at[idx, "suggested_website"] = website
                df.at[idx, "source_url"] = source
                df.at[idx, "confidence"] = confidence
                df.at[idx, "review_status"] = "Website Found"
                df.at[idx, "ready_to_merge"] = "Yes"
                df.at[idx, "notes"] = "Interactive Website Discovery"

                df.to_csv(OUTPUT_FILE, index=False)

                print("✓ Saved")
                break

            elif choice == "k":

                df.at[idx, "review_status"] = "Skipped"
                df.at[idx, "ready_to_merge"] = "No"

                df.to_csv(OUTPUT_FILE, index=False)

                print("✓ Skipped")
                break

            elif choice == "q":

                df.to_csv(OUTPUT_FILE, index=False)

                print()
                print("Progress saved.")
                print("Results:", OUTPUT_FILE)

                return

            else:
                print("Invalid option.")

    df.to_csv(OUTPUT_FILE, index=False)

    print()
    print("=" * 60)
    print("Batch Complete!")
    print("=" * 60)
    print("Results saved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    run()
    