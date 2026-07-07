from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from config import MASTER_FILE
from app.restaurant_intelligence.config import RESULTS_FOLDER, TARGET_FIELDS


def latest_results_file():
    files = sorted(RESULTS_FOLDER.glob("*_results.csv"))
    if not files:
        print("No restaurant intelligence results files found.")
        return None
    return files[-1]


def yes(value):
    return str(value).strip().lower() in {"yes", "y", "true", "1"}


def show_merge_preview():
    results_file = latest_results_file()
    if results_file is None:
        return

    master = pd.read_excel(MASTER_FILE, dtype=str)
    results = pd.read_csv(results_file, dtype=str)

    approved = results[results["ready_to_merge"].apply(yes)].copy()

    if approved.empty:
        print("No restaurant intelligence rows marked ready_to_merge = Yes.")
        return

    master_lookup = master.set_index("business_id").to_dict("index")

    print("=" * 80)
    print("Restaurant Intelligence Merge Preview")
    print("=" * 80)
    print("Results file:", results_file.name)

    for _, row in approved.iterrows():
        business_id = row["business_id"]
        master_row = master_lookup.get(business_id, {})

        print("-" * 80)
        print("Business:", row.get("post_title", ""))
        print("Business ID:", business_id)

        for field in TARGET_FIELDS:
            suggested_field = f"suggested_{field}"

            if suggested_field not in row:
                continue

            current = master_row.get(field, "")
            suggested = row.get(suggested_field, "")

            if str(suggested).strip() and str(suggested).strip().lower() != "nan":
                print(f"{field}:")
                print("  Current:", current)
                print("  Suggested:", suggested)

        print("Confidence:", row.get("confidence", ""))
        print("Notes:", row.get("notes", ""))

    print("=" * 80)
    print(f"Approved rows ready to merge: {len(approved)}")


if __name__ == "__main__":
    show_merge_preview()
