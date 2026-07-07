from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from config import MASTER_FILE
from utils import is_blank, timestamp

QUEUE_FOLDER = ROOT / "enrichment" / "queues"

def build_missing_website_queue():
    print("Building missing website queue...")

    QUEUE_FOLDER.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(MASTER_FILE)

    if "website" not in df.columns:
        print("Missing required column: website")
        raise SystemExit(1)

    missing = df[df["website"].apply(is_blank)].copy()

    useful_columns = [
        "business_id",
        "post_title",
        "town",
        "county",
        "phone",
        "email",
        "primary_category",
        "primary_business_type",
    ]

    available = [col for col in useful_columns if col in missing.columns]
    queue = missing[available].copy()

    queue["research_status"] = "Needs Website"
    queue["suggested_website"] = ""
    queue["source_url"] = ""
    queue["confidence"] = ""
    queue["notes"] = ""

    out_path = QUEUE_FOLDER / f"missing_websites_queue_{timestamp()}.csv"
    queue.to_csv(out_path, index=False)

    print("Queue created:", out_path)
    print(f"Businesses missing website: {len(queue):,}")

if __name__ == "__main__":
    build_missing_website_queue()
