from pathlib import Path
import sys
from datetime import datetime
import shutil
import os
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from config import MASTER_FILE, BACKUP_FOLDER, REPORT_FOLDER
from app.auto_fix.config import AUTO_FIX_PREVIEW_FILE, AUTO_FIX_REPORT_FILE


def is_blank(value):
    return pd.isna(value) or str(value).strip().lower() in {"", "nan", "null", "none"}


def yes(value):
    return str(value).strip().lower() in {"yes", "y", "true", "1"}


def apply_county_fixes():
    if not AUTO_FIX_PREVIEW_FILE.exists():
        print("No auto-fix preview file found. Run:")
        print("python3 -m app.auto_fix.county_fix")
        return

    master = pd.read_excel(MASTER_FILE, dtype=str)
    preview = pd.read_csv(AUTO_FIX_PREVIEW_FILE, dtype=str)

    ready = preview[preview["ready_to_apply"].apply(yes)].copy()

    if ready.empty:
        print("No fixes marked ready_to_apply = Yes.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    BACKUP_FOLDER.mkdir(parents=True, exist_ok=True)
    REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

    backup_file = BACKUP_FOLDER / f"203local_Master_Auto_Fix_Backup_{timestamp}.xlsx"
    report_file = REPORT_FOLDER / f"Auto_Fix_Report_{timestamp}.csv"
    temp_file = MASTER_FILE.with_suffix(".tmp.xlsx")

    shutil.copy2(MASTER_FILE, backup_file)

    master_ids = set(master["business_id"])
    report_rows = []
    applied = 0
    skipped = 0

    for _, fix in ready.iterrows():
        business_id = fix.get("business_id", "")
        suggested_county = fix.get("suggested_county", "")

        if business_id not in master_ids:
            skipped += 1
            report_rows.append({
                "business_id": business_id,
                "status": "Skipped",
                "reason": "Business ID not found",
            })
            continue

        idx = master.index[master["business_id"] == business_id][0]
        current_county = master.at[idx, "county"]

        if not is_blank(current_county):
            skipped += 1
            report_rows.append({
                "business_id": business_id,
                "status": "Skipped",
                "reason": "County already populated",
            })
            continue

        master.at[idx, "county"] = suggested_county
        applied += 1

        report_rows.append({
            "business_id": business_id,
            "post_title": fix.get("post_title", ""),
            "town": fix.get("town", ""),
            "status": "Applied",
            "field": "county",
            "old_value": current_county,
            "new_value": suggested_county,
            "reason": "County derived from town",
        })

    pd.DataFrame(report_rows).to_csv(report_file, index=False)

    if applied > 0:
        print("Writing updated master to temporary file...")
        master.to_excel(temp_file, index=False)

        print("Verifying temporary file...")
        test = pd.read_excel(temp_file)
        if len(test) != len(master):
            raise RuntimeError("Temporary master verification failed. Row count mismatch.")

        print("Replacing master file...")
        os.replace(temp_file, MASTER_FILE)
    else:
        print("No fixes applied, so Master Directory was not modified.")

    print("=" * 70)
    print("Auto-Fix Complete")
    print("=" * 70)
    print("Preview file:", AUTO_FIX_PREVIEW_FILE)
    print("Backup created:", backup_file)
    print("Report created:", report_file)
    print("Applied:", applied)
    print("Skipped:", skipped)


if __name__ == "__main__":
    apply_county_fixes()
