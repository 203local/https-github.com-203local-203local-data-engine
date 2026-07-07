from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from config import MASTER_FILE
from app.ai_enrichment.config import QUEUE_FILE, BATCH_FOLDER, TARGET_FIELDS


def is_blank(value):
    return pd.isna(value) or str(value).strip() == ""


def generate_ai_queue():
    BATCH_FOLDER.mkdir(parents=True, exist_ok=True)

    master = pd.read_excel(MASTER_FILE, dtype=str)

    eligible = master[
        master["website"].apply(lambda x: not is_blank(x))
        & (
            master["post_content"].apply(is_blank)
            | master["seo_meta_description"].apply(is_blank)
            | master["seo_directory_title"].apply(is_blank)
        )
    ].copy()

    base_columns = [
        "business_id",
        "post_title",
        "town",
        "county",
        "website",
        "primary_category",
        "primary_business_type",
    ]

    queue = eligible[base_columns + TARGET_FIELDS].copy()

    queue["suggested_post_content"] = ""
    queue["suggested_seo_directory_title"] = ""
    queue["suggested_seo_meta_description"] = ""
    queue["suggested_searchable_keywords"] = ""
    queue["suggested_restaurant_intelligence_notes"] = ""
    queue["source_url"] = ""
    queue["confidence"] = ""
    queue["review_status"] = "Needs Review"
    queue["ready_to_merge"] = "No"
    queue["notes"] = ""

    queue.to_csv(QUEUE_FILE, index=False)

    print("=" * 70)
    print("AI Enrichment Queue Created")
    print("=" * 70)
    print("Master file:", MASTER_FILE)
    print("Eligible businesses:", len(queue))
    print("Queue file:", QUEUE_FILE)


if __name__ == "__main__":
    generate_ai_queue()
