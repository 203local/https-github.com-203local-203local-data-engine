from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from config import MASTER_FILE
from app.email_discovery.config import RESULTS_FOLDER


def latest_results_file():
    files = sorted(RESULTS_FOLDER.glob("*_interactive_results.csv"))
    if not files:
        print("No email results files found.")
        return None
    return files[-1]


def yes(value):
    return str(value).strip().lower() in {"yes", "y", "true", "1"}


def show_merge_preview():
    results_file = latest_results_file()

    if results_file is None:
        return

    master = pd.read_excel(MASTER_FILE)
    results = pd.read_csv(results_file)

    approved = results[results["ready_to_merge"].apply(yes)].copy()

    if approved.empty:
        print("No rows marked ready_to_merge = Yes.")
        return

    master_lookup = master.set_index("business_id").to_dict("index")

    print("=" * 80)
    print("Email Merge Preview")
    print("=" * 80)
    print("Results file:", results_file.name)
    print()

    for _, row in approved.iterrows():
        business_id = row["business_id"]
        master_row = master_lookup.get(business_id, {})

        print("-" * 80)
        print("Business:", row.get("post_title", ""))
        print("Business ID:", business_id)
        print("Current email:", master_row.get("email", ""))
        print("Suggested email:", row.get("suggested_email", ""))
        print("Confidence:", row.get("confidence", ""))
        print("Source:", row.get("source_url", ""))
        print("Notes:", row.get("notes", ""))

    print("=" * 80)
    print(f"Approved rows ready to merge: {len(approved)}")


if __name__ == "__main__":
    show_merge_preview()
