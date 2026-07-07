from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from config import MASTER_FILE, BACKUP_FOLDER, REPORT_FOLDER, TEMP_FOLDER
from scripts.safe_save import safe_write_excel
from scripts.change_log import log_event
from utils import normalize_text, normalize_key, is_blank, timestamp

TOWN_REFERENCE_FILE = ROOT / "reference" / "ct_towns.csv"
ALIAS_REFERENCE_FILE = ROOT / "reference" / "ct_place_aliases.csv"

def build_geography_lookup():
    lookup = {}

    if TOWN_REFERENCE_FILE.exists():
        towns = pd.read_csv(TOWN_REFERENCE_FILE)
        towns.columns = [str(c).strip().lower() for c in towns.columns]
        for _, row in towns.iterrows():
            lookup[normalize_key(row.get("town"))] = {
                "county": row.get("county"),
                "parent_town": row.get("town"),
                "match_type": "official_town"
            }

    if ALIAS_REFERENCE_FILE.exists():
        aliases = pd.read_csv(ALIAS_REFERENCE_FILE)
        aliases.columns = [str(c).strip().lower() for c in aliases.columns]
        for _, row in aliases.iterrows():
            lookup[normalize_key(row.get("place_name"))] = {
                "county": row.get("county"),
                "parent_town": row.get("parent_town"),
                "match_type": "alias"
            }

    return lookup

def autofill_counties():
    print("Running County Auto-Fill with geography aliases...")

    lookup = build_geography_lookup()

    if not lookup:
        print("No geography reference data found.")
        print("Required files:")
        print("reference/ct_towns.csv")
        print("optional: reference/ct_place_aliases.csv")
        raise SystemExit(1)

    df = pd.read_excel(MASTER_FILE)

    if "town" not in df.columns or "county" not in df.columns:
        print("Master must include town and county columns.")
        raise SystemExit(1)

    changes = []
    unmatched = []

    for idx, row in df.iterrows():
        town = normalize_text(row.get("town"))
        county = normalize_text(row.get("county"))

        if not is_blank(county):
            continue

        match = lookup.get(normalize_key(town))

        if match and match.get("county"):
            df.at[idx, "county"] = match["county"]
            changes.append({
                "row_number_excel": idx + 2,
                "business": row.get("post_title", ""),
                "town": town,
                "old_county": county,
                "new_county": match["county"],
                "parent_town": match.get("parent_town", ""),
                "match_type": match.get("match_type", "")
            })
        else:
            unmatched.append({
                "row_number_excel": idx + 2,
                "business": row.get("post_title", ""),
                "town": town,
                "reason": "Town/place not found in reference"
            })

    save_info = None
    if changes:
        save_info = safe_write_excel(df, MASTER_FILE, BACKUP_FOLDER, TEMP_FOLDER)
        print("Safe save complete.")
        print("Backup:", save_info["backup_path"])
    else:
        print("No blank counties could be filled.")

    REPORT_FOLDER.mkdir(exist_ok=True)
    report_path = REPORT_FOLDER / f"County_Autofill_Report_{timestamp()}.xlsx"

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        pd.DataFrame([{
            "counties_filled": len(changes),
            "unmatched_rows": len(unmatched),
            "backup_file": save_info["backup_path"] if save_info else "",
        }]).to_excel(writer, sheet_name="Summary", index=False)
        pd.DataFrame(changes).to_excel(writer, sheet_name="Filled Counties", index=False)
        pd.DataFrame(unmatched).to_excel(writer, sheet_name="Unmatched Towns", index=False)

    log_event("County Auto-Fill", f"Filled {len(changes)} counties using towns + aliases. Unmatched: {len(unmatched)}", len(changes))

    print("County Auto-Fill complete.")
    print("Counties filled:", len(changes))
    print("Unmatched rows:", len(unmatched))
    print("Report created:", report_path)

if __name__ == "__main__":
    autofill_counties()
