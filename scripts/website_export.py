from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from config import EXPORT_FOLDER
from scripts.master_loader import load_master
from scripts.field_dictionary_loader import get_website_export_fields
from scripts.change_log import log_event
from utils import timestamp, is_blank

def export_website_csv():
    print("Creating website export...")

    df = load_master(create_backup=True)
    EXPORT_FOLDER.mkdir(exist_ok=True)

    fields = get_website_export_fields()

    if not fields:
        print("No website export fields found in field dictionary.")
        return

    available = [field for field in fields if field in df.columns]
    missing = [field for field in fields if field not in df.columns]

    export_df = df[available].copy()

    if "post_title" in export_df.columns:
        export_df = export_df[~export_df["post_title"].apply(is_blank)]

    out_path = EXPORT_FOLDER / f"Website_Export_{timestamp()}.csv"
    export_df.to_csv(out_path, index=False)

    log_event(
        "Website Export",
        f"Created website export: {out_path.name}. Missing fields: {missing}",
        len(export_df)
    )

    print("Website export created:", out_path)
    print(f"Rows exported: {len(export_df):,}")

    if missing:
        print("Missing fields from master:", ", ".join(missing))

if __name__ == "__main__":
    export_website_csv()
