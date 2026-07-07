from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from config import MASTER_FILE, BACKUP_FOLDER, REPORT_FOLDER, TEMP_FOLDER
from scripts.safe_save import safe_write_excel
from scripts.change_log import log_event
from utils import normalize_text, is_blank, timestamp

RESULTS_FOLDER = ROOT / "enrichment" / "results"

# These result columns are workflow metadata and should not be merged into the master.
CONTROL_COLUMNS = {
    "research_status",
    "source_url",
    "confidence",
    "notes",
    "google_search_query",
    "google_search_url",
    "maps_search_query",
    "official_site_guess",
    "review_status",
    "ready_to_merge",
}

# Maps enrichment result columns to master columns.
# Add more mappings here as future enrichment modules are built.
FIELD_MAP = {
    "suggested_website": "website",
    "suggested_email": "email",
    "suggested_phone": "phone",
    "suggested_instagram": "instagram",
    "suggested_facebook": "facebook",
    "suggested_tiktok": "tiktok",
    "suggested_linkedin": "linkedin",
    "suggested_youtube": "youtube",
    "suggested_menu_link": "menu_link",
    "suggested_reservation_link": "reservation_link",
    "suggested_reservation_platform": "reservation_platform",
    "suggested_delivery_platforms": "delivery_platforms",
}

def latest_results_file():
    files = sorted(RESULTS_FOLDER.glob("*_results.csv"))
    if not files:
        print("No results files found in:", RESULTS_FOLDER)
        raise SystemExit(1)
    return files[-1]

def yes(value):
    return normalize_text(value).lower() in {"yes", "y", "true", "1", "x"}

def merge_results(results_file=None, overwrite=False):
    print("Running Generic Merge Manager...")

    if results_file is None:
        results_file = latest_results_file()
    else:
        results_file = Path(results_file)

    print("Results file:", results_file)

    if not results_file.exists():
        print("Results file not found:", results_file)
        raise SystemExit(1)

    master = pd.read_excel(MASTER_FILE)
    results = pd.read_csv(results_file)

    if "business_id" not in master.columns:
        print("Master is missing required column: business_id")
        raise SystemExit(1)

    if "business_id" not in results.columns:
        print("Results file is missing required column: business_id")
        raise SystemExit(1)

    if "ready_to_merge" not in results.columns:
        print("Results file is missing required column: ready_to_merge")
        raise SystemExit(1)

    approved = results[results["ready_to_merge"].apply(yes)].copy()

    if approved.empty:
        print("No rows marked ready_to_merge = Yes.")
        return

    master_index = {
        normalize_text(row["business_id"]): idx
        for idx, row in master.iterrows()
    }

    changes = []
    skipped = []
    unmatched = []

    for _, row in approved.iterrows():
        business_id = normalize_text(row.get("business_id"))
        master_idx = master_index.get(business_id)

        if master_idx is None:
            unmatched.append({
                "business_id": business_id,
                "post_title": row.get("post_title", ""),
                "reason": "business_id not found in master"
            })
            continue

        for source_col, target_col in FIELD_MAP.items():
            if source_col not in results.columns:
                continue
            if target_col not in master.columns:
                skipped.append({
                    "business_id": business_id,
                    "post_title": row.get("post_title", ""),
                    "source_col": source_col,
                    "target_col": target_col,
                    "reason": "target column missing in master"
                })
                continue

            new_value = normalize_text(row.get(source_col))
            if is_blank(new_value):
                continue

            old_value = normalize_text(master.at[master_idx, target_col])

            if not overwrite and not is_blank(old_value):
                skipped.append({
                    "business_id": business_id,
                    "post_title": row.get("post_title", ""),
                    "field": target_col,
                    "old_value": old_value,
                    "new_value": new_value,
                    "reason": "master already has value; overwrite disabled"
                })
                continue

            if old_value == new_value:
                continue

            master.at[master_idx, target_col] = new_value
            changes.append({
                "business_id": business_id,
                "post_title": master.at[master_idx, "post_title"] if "post_title" in master.columns else row.get("post_title", ""),
                "field": target_col,
                "old_value": old_value,
                "new_value": new_value,
                "source_column": source_col,
                "source_url": row.get("source_url", ""),
                "confidence": row.get("confidence", ""),
                "notes": row.get("notes", ""),
            })

    save_info = None
    if changes:
        save_info = safe_write_excel(master, MASTER_FILE, BACKUP_FOLDER, TEMP_FOLDER)
        print("Safe save complete.")
        print("Backup:", save_info["backup_path"])
    else:
        print("No changes to save.")

    REPORT_FOLDER.mkdir(exist_ok=True)
    report_path = REPORT_FOLDER / f"Generic_Merge_Report_{timestamp()}.xlsx"

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        pd.DataFrame([{
            "results_file": str(results_file),
            "approved_rows": len(approved),
            "changes_applied": len(changes),
            "skipped": len(skipped),
            "unmatched": len(unmatched),
            "overwrite_enabled": overwrite,
            "backup_file": save_info["backup_path"] if save_info else "",
        }]).to_excel(writer, sheet_name="Summary", index=False)

        pd.DataFrame(changes).to_excel(writer, sheet_name="Changes Applied", index=False)
        pd.DataFrame(skipped).to_excel(writer, sheet_name="Skipped", index=False)
        pd.DataFrame(unmatched).to_excel(writer, sheet_name="Unmatched", index=False)

    log_event(
        "Generic Merge",
        f"Merged {len(changes)} field changes from {results_file.name}. Skipped: {len(skipped)}. Unmatched: {len(unmatched)}",
        len(changes)
    )

    print("Merge complete.")
    print("Approved rows:", len(approved))
    print("Changes applied:", len(changes))
    print("Skipped:", len(skipped))
    print("Unmatched:", len(unmatched))
    print("Report created:", report_path)

if __name__ == "__main__":
    merge_results()
