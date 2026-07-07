from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from config import MASTER_FILE
from app.auto_fix.config import TOWN_TO_COUNTY, AUTO_FIX_PREVIEW_FILE, REPORT_FOLDER


def is_blank(value):
    return pd.isna(value) or str(value).strip().lower() in {"", "nan", "null", "none"}


def normalize_town(value):
    return str(value).strip().lower()


def preview_county_fixes():
    REPORT_FOLDER.mkdir(parents=True, exist_ok=True)

    master = pd.read_excel(MASTER_FILE, dtype=str)

    rows = []

    for _, row in master.iterrows():
        town = row.get("town", "")
        county = row.get("county", "")

        if not is_blank(county):
            continue

        town_key = normalize_town(town)
        suggested_county = TOWN_TO_COUNTY.get(town_key)

        if suggested_county:
            rows.append({
                "business_id": row.get("business_id", ""),
                "post_title": row.get("post_title", ""),
                "town": town,
                "current_county": county,
                "suggested_county": suggested_county,
                "fix_type": "county_from_town",
                "ready_to_apply": "Yes",
            })

    preview = pd.DataFrame(rows)
    preview.to_csv(AUTO_FIX_PREVIEW_FILE, index=False)

    print("=" * 70)
    print("County Auto-Fix Preview Created")
    print("=" * 70)
    print("Fixes found:", len(preview))
    print("Preview file:", AUTO_FIX_PREVIEW_FILE)

    if not preview.empty:
        print()
        print(preview.head(25).to_string(index=False))


if __name__ == "__main__":
    preview_county_fixes()
