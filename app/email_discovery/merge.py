from pathlib import Path
import sys
from datetime import datetime
import shutil
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from config import MASTER_FILE, BACKUP_FOLDER, REPORT_FOLDER
from app.email_discovery.config import RESULTS_FOLDER
from app.email_discovery.validation import is_valid_email


def latest_results_file():
    files = sorted(RESULTS_FOLDER.glob("*_interactive_results.csv"))
    if not files:
        print("No email results files found.")
        return None
    return files[-1]


def yes(value):
    return str(value).strip().lower() in {"yes", "y", "true", "1"}


def merge_emails():
    results_file = latest_results_file()

    if results_file is None:
        return

    master = pd.read_excel(MASTER_FILE)
    results = pd.read_csv(results_file)

    approved = results[results["ready_to_merge"].apply(yes)].copy()

    if approved.empty:
        print("No approved email rows to merge.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    BACKUP_FOLDER.mkdir(parents=True, exist_ok=True)
    REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

    backup_file = BACKUP_FOLDER / f"203local_Master_Email_Merge_Backup_{timestamp}.xlsx"
    report_file = REPORT_FOLDER / f"Email_Merge_Report_{timestamp}.csv"

    shutil.copy2(MASTER_FILE, backup_file)

    report_rows = []
    merged_count = 0
    skipped_count = 0

    master_ids = set(master["business_id"])

    for _, row in approved.iterrows():
        business_id = row.get("business_id")
        suggested_email = str(row.get("suggested_email", "")).strip()

        valid, reason = is_valid_email(suggested_email)

        if business_id not in master_ids:
            skipped_count += 1
            report_rows.append({
                "business_id": business_id,
                "business": row.get("post_title", ""),
                "suggested_email": suggested_email,
                "status": "Skipped",
                "reason": "Business ID not found",
            })
            continue

        if not valid:
            skipped_count += 1
            report_rows.append({
                "business_id": business_id,
                "business": row.get("post_title", ""),
                "suggested_email": suggested_email,
                "status": "Skipped",
                "reason": reason,
            })
            continue

        idx = master.index[master["business_id"] == business_id][0]
        current_email = master.at[idx, "email"]

        if pd.notna(current_email) and str(current_email).strip():
            skipped_count += 1
            report_rows.append({
                "business_id": business_id,
                "business": row.get("post_title", ""),
                "suggested_email": suggested_email,
                "status": "Skipped",
                "reason": "Master already has email",
            })
            continue

        master.at[idx, "email"] = suggested_email
        merged_count += 1

        report_rows.append({
            "business_id": business_id,
            "business": row.get("post_title", ""),
            "suggested_email": suggested_email,
            "status": "Merged",
            "reason": "Merged successfully",
        })

    master.to_excel(MASTER_FILE, index=False)
    pd.DataFrame(report_rows).to_csv(report_file, index=False)

    print("=" * 70)
    print("Email Merge Complete")
    print("=" * 70)
    print("Results file:", results_file)
    print("Backup created:", backup_file)
    print("Report created:", report_file)
    print("Merged:", merged_count)
    print("Skipped:", skipped_count)


if __name__ == "__main__":
    merge_emails()
