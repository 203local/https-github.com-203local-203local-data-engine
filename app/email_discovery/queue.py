from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from config import MASTER_FILE
from app.email_discovery.config import BATCH_FOLDER


QUEUE_FILE = BATCH_FOLDER / "missing_emails_queue.csv"


def is_blank(value):
    return pd.isna(value) or str(value).strip() == ""


def generate_email_queue():
    BATCH_FOLDER.mkdir(parents=True, exist_ok=True)

    master = pd.read_excel(MASTER_FILE)

    missing = master[master["email"].apply(is_blank)].copy()

    columns = [
        "business_id",
        "post_title",
        "town",
        "county",
        "phone",
        "website",
        "email",
    ]

    queue = missing[columns].copy()

    queue["suggested_email"] = ""
    queue["source_url"] = ""
    queue["confidence"] = ""
    queue["review_status"] = "Needs Review"
    queue["ready_to_merge"] = "No"
    queue["notes"] = ""

    queue.to_csv(QUEUE_FILE, index=False)

    print("=" * 70)
    print("Email Discovery Queue Created")
    print("=" * 70)
    print("Master file:", MASTER_FILE)
    print("Missing emails:", len(queue))
    print("Queue file:", QUEUE_FILE)


if __name__ == "__main__":
    generate_email_queue()
