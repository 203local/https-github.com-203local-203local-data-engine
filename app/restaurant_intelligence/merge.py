from pathlib import Path
import sys
from datetime import datetime
import shutil
import os
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from config import MASTER_FILE, BACKUP_FOLDER, REPORT_FOLDER
from app.restaurant_intelligence.config import RESULTS_FOLDER, TARGET_FIELDS


def latest_results_file():
    files = sorted(RESULTS_FOLDER.glob("*_results.csv"))
    return files[-1] if files else None


def yes(value):
    return str(value).strip().lower() in {"yes", "y", "true", "1"}


def has_value(value):
    return pd.notna(value) and str(value).strip().lower() not in {"", "nan", "null", "none", "[]"}


def normalize_set(value):
    if not has_value(value):
        return set()

    text = str(value).strip()

    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return {str(x).strip().lower() for x in parsed if str(x).strip()}
    except Exception:
        pass

    return {x.strip().lower() for x in text.split(",") if x.strip()}


def equivalent(current, suggested):
    return normalize_set(current) == normalize_set(suggested)


def merge_restaurant_intelligence():
    results_file = latest_results_file()

    if results_file is None:
        print("No restaurant intelligence results files found.")
        return

    master = pd.read_excel(MASTER_FILE, dtype=str)
    results = pd.read_csv(results_file, dtype=str)

    approved = results[results["ready_to_merge"].apply(yes)].copy()

    if approved.empty:
        print("No approved restaurant intelligence rows to merge.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    BACKUP_FOLDER.mkdir(parents=True, exist_ok=True)
    REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

    backup_file = BACKUP_FOLDER / f"203local_Master_Restaurant_Intelligence_Backup_{timestamp}.xlsx"
    report_file = REPORT_FOLDER / f"Restaurant_Intelligence_Merge_Report_{timestamp}.csv"
    temp_file = MASTER_FILE.with_suffix(".tmp.xlsx")

    shutil.copy2(MASTER_FILE, backup_file)

    master_ids = set(master["business_id"])
    report_rows = []
    merged_rows = 0
    skipped_rows = 0

    for _, row in approved.iterrows():
        business_id = row.get("business_id")
        business = row.get("post_title", "")

        if business_id not in master_ids:
            skipped_rows += 1
            report_rows.append({
                "business_id": business_id,
                "business": business,
                "status": "Skipped",
                "reason": "Business ID not found",
            })
            continue

        idx = master.index[master["business_id"] == business_id][0]
        updated_fields = []
        skipped_fields = []

        for field in TARGET_FIELDS:
            suggested_field = f"suggested_{field}"

            if suggested_field not in row:
                continue

            suggested = row.get(suggested_field, "")
            current = master.at[idx, field] if field in master.columns else ""

            if not has_value(suggested):
                continue

            # Preserve existing curated data. Only fill blanks.
            if has_value(current):
                if equivalent(current, suggested):
                    skipped_fields.append(f"{field}: equivalent")
                else:
                    skipped_fields.append(f"{field}: already populated")
                continue

            master.at[idx, field] = suggested
            updated_fields.append(field)

        if updated_fields:
            merged_rows += 1
            report_rows.append({
                "business_id": business_id,
                "business": business,
                "status": "Merged",
                "updated_fields": ", ".join(updated_fields),
                "skipped_fields": ", ".join(skipped_fields),
            })
        else:
            skipped_rows += 1
            report_rows.append({
                "business_id": business_id,
                "business": business,
                "status": "Skipped",
                "updated_fields": "",
                "skipped_fields": ", ".join(skipped_fields),
            })

    pd.DataFrame(report_rows).to_csv(report_file, index=False)

    if merged_rows > 0:
        print("Writing updated master to temporary file...")
        master.to_excel(temp_file, index=False)

        print("Verifying temporary file...")
        test = pd.read_excel(temp_file)
        if len(test) != len(master):
            raise RuntimeError("Temporary master verification failed. Row count mismatch.")

        print("Replacing master file...")
        os.replace(temp_file, MASTER_FILE)
    else:
        print("No restaurant intelligence fields merged, so Master Directory was not modified.")

    print("=" * 70)
    print("Restaurant Intelligence Merge Complete")
    print("=" * 70)
    print("Results file:", results_file)
    print("Backup created:", backup_file)
    print("Report created:", report_file)
    print("Merged rows:", merged_rows)
    print("Skipped rows:", skipped_rows)


if __name__ == "__main__":
    merge_restaurant_intelligence()
