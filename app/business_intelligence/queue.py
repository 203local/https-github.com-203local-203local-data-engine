from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from config import MASTER_FILE
from app.business_intelligence.config import QUEUE_FILE, BATCH_FOLDER, TARGET_FIELDS


def is_blank(value):
    return pd.isna(value) or str(value).strip().lower() in {"", "nan", "null", "none"}


def needs_business_intelligence(row):
    important_fields = [
        "business_types",
        "offerings_tags",
        "service_tags",
        "amenities_tags",
        "audience_tags",
        "searchable_keywords",
    ]

    return any(is_blank(row.get(field, "")) for field in important_fields)


def generate_business_intelligence_queue():
    BATCH_FOLDER.mkdir(parents=True, exist_ok=True)

    master = pd.read_excel(MASTER_FILE, dtype=str)

    eligible = master[
        master["website"].apply(lambda x: not is_blank(x))
        & master.apply(needs_business_intelligence, axis=1)
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

    suggested_fields = [
        "suggested_primary_category",
        "suggested_primary_business_type",
        "suggested_business_types",
        "suggested_offerings_tags",
        "suggested_service_tags",
        "suggested_amenities_tags",
        "suggested_audience_tags",
        "suggested_ownership_tags",
        "suggested_service_model_tags",
        "suggested_searchable_keywords",
        "suggested_business_intelligence_notes",
    ]

    for field in suggested_fields:
        queue[field] = ""

    queue["source_url"] = ""
    queue["confidence"] = ""
    queue["review_status"] = "Needs Review"
    queue["ready_to_merge"] = "No"
    queue["notes"] = ""

    queue.to_csv(QUEUE_FILE, index=False)

    print("=" * 70)
    print("Business Intelligence Queue Created")
    print("=" * 70)
    print("Master file:", MASTER_FILE)
    print("Eligible businesses:", len(queue))
    print("Queue file:", QUEUE_FILE)


if __name__ == "__main__":
    generate_business_intelligence_queue()
