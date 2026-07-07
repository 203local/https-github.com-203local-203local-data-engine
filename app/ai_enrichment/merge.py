from pathlib import Path
import sys
from datetime import datetime
import shutil
import os
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from config import MASTER_FILE, BACKUP_FOLDER, REPORT_FOLDER
from app.ai_enrichment.config import RESULTS_FOLDER


MERGE_FIELDS = {
    "post_content": "suggested_post_content",
    "seo_directory_title": "suggested_seo_directory_title",
    "seo_meta_description": "suggested_seo_meta_description",
    "searchable_keywords": "suggested_searchable_keywords",
    "restaurant_intelligence_notes": "notes",
    "restaurant_intelligence_source": "source_url",
}


def latest_results_file():
    files = sorted(RESULTS_FOLDER.glob("*_results.csv"))
    if not files:
        print("No AI results files found.")
        return None
    return files[-1]


def yes(value):
    return str(value).strip().lower() in {"yes", "y", "true", "1"}


def has_value(value):
    return pd.notna(value) and str(value).strip() not in {"", "nan"}


def merge_ai_enrichment():
    results_file = latest_results_file()
    if results_file is None:
        return

    master = pd.read_excel(MASTER_FILE, dtype=str)
    results = pd.read_csv(results_file, dtype=str)

    approved = results[results["ready_to_merge"].apply(yes)].copy()

    if approved.empty:
        print("No approved AI rows to merge.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    BACKUP_FOLDER.mkdir(parents=True, exist_ok=True)
    REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

    backup_file = BACKUP_FOLDER / f"203local_Master_AI_Merge_Backup_{timestamp}.xlsx"
    report_file = REPORT_FOLDER / f"AI_Merge_Report_{timestamp}.csv"
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
        fields_updated = []

        for master_field, suggested_field in MERGE_FIELDS.items():
            suggested_value = row.get(suggested_field, "")

            if not has_value(suggested_value):
                continue

            current_value = master.at[idx, master_field] if master_field in master.columns else ""

            if has_value(current_value):
                continue

            master.at[idx, master_field] = suggested_value
            fields_updated.append(master_field)

        if fields_updated:
            merged_rows += 1
            report_rows.append({
                "business_id": business_id,
                "business": business,
                "status": "Merged",
                "reason": "Updated fields: " + ", ".join(fields_updated),
            })
        else:
            skipped_rows += 1
            report_rows.append({
                "business_id": business_id,
                "business": business,
                "status": "Skipped",
                "reason": "No blank target fields to update",
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
        print("No AI fields merged, so Master Directory was not modified.")

    print("=" * 70)
    print("AI Enrichment Merge Complete")
    print("=" * 70)
    print("Results file:", results_file)
    print("Backup created:", backup_file)
    print("Report created:", report_file)
    print("Merged rows:", merged_rows)
    print("Skipped rows:", skipped_rows)


if __name__ == "__main__":
    merge_ai_enrichment()
