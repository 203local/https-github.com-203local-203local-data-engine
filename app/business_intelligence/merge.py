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
from app.business_intelligence.config import RESULTS_FOLDER


SAFE_MERGE_FIELDS = [
    "business_types",
    "offerings_tags",
    "service_tags",
    "amenities_tags",
    "audience_tags",
    "ownership_tags",
    "service_model_tags",
    "searchable_keywords",
]


PROTECTED_FIELDS = [
    "primary_category",
    "primary_business_type",
]


def latest_results_file():
    files = sorted(RESULTS_FOLDER.glob("*_results.csv"))
    return files[-1] if files else None


def yes(value):
    return str(value).strip().lower() in {"yes", "y", "true", "1"}


def has_value(value):
    return pd.notna(value) and str(value).strip().lower() not in {"", "nan", "null", "none", "[]"}


def parse_values(value):
    if not has_value(value):
        return []

    text = str(value).strip()

    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(x).strip() for x in parsed if str(x).strip()]
    except Exception:
        pass

    return [x.strip() for x in text.split(",") if x.strip()]


def merge_lists(current, suggested):
    current_items = parse_values(current)
    suggested_items = parse_values(suggested)

    combined = []
    seen = set()

    for item in current_items + suggested_items:
        key = item.lower()
        if key not in seen:
            combined.append(item)
            seen.add(key)

    return ", ".join(combined)


def merge_business_intelligence():
    results_file = latest_results_file()

    if results_file is None:
        print("No business intelligence results files found.")
        return

    master = pd.read_excel(MASTER_FILE, dtype=str)
    results = pd.read_csv(results_file, dtype=str)

    approved = results[results["ready_to_merge"].apply(yes)].copy()

    if approved.empty:
        print("No approved business intelligence rows to merge.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    BACKUP_FOLDER.mkdir(parents=True, exist_ok=True)
    REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

    backup_file = BACKUP_FOLDER / f"203local_Master_Business_Intelligence_Backup_{timestamp}.xlsx"
    report_file = REPORT_FOLDER / f"Business_Intelligence_Merge_Report_{timestamp}.csv"
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
        protected_flags = []

        for field in SAFE_MERGE_FIELDS:
            suggested = row.get(f"suggested_{field}", "")
            current = master.at[idx, field] if field in master.columns else ""

            if not has_value(suggested):
                continue

            merged_value = merge_lists(current, suggested)

            if merged_value and merged_value != str(current).strip():
                master.at[idx, field] = merged_value
                updated_fields.append(field)

        for field in PROTECTED_FIELDS:
            suggested = row.get(f"suggested_{field}", "")
            current = master.at[idx, field] if field in master.columns else ""

            if has_value(suggested) and has_value(current) and str(suggested).strip() != str(current).strip():
                protected_flags.append(f"{field}: current='{current}' suggested='{suggested}'")

        notes = row.get("suggested_business_intelligence_notes", "") or row.get("notes", "")
        if has_value(notes) and "restaurant_intelligence_notes" in master.columns:
            current_notes = master.at[idx, "restaurant_intelligence_notes"]
            if not has_value(current_notes):
                master.at[idx, "restaurant_intelligence_notes"] = notes
                updated_fields.append("restaurant_intelligence_notes")

        if updated_fields:
            merged_rows += 1
            status = "Merged"
        else:
            skipped_rows += 1
            status = "Skipped"

        report_rows.append({
            "business_id": business_id,
            "business": business,
            "status": status,
            "updated_fields": ", ".join(updated_fields),
            "protected_flags": " | ".join(protected_flags),
            "review_needed": row.get("suggested_review_needed", ""),
            "existing_data_conflict": row.get("suggested_existing_data_conflict", ""),
            "review_reason": row.get("suggested_review_reason", ""),
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
        print("No business intelligence fields merged, so Master Directory was not modified.")

    print("=" * 70)
    print("Business Intelligence Merge Complete")
    print("=" * 70)
    print("Results file:", results_file)
    print("Backup created:", backup_file)
    print("Report created:", report_file)
    print("Merged rows:", merged_rows)
    print("Skipped rows:", skipped_rows)


if __name__ == "__main__":
    merge_business_intelligence()
