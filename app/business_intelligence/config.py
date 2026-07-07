from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

BATCH_FOLDER = ROOT / "enrichment" / "business_intelligence_batches"
RESULTS_FOLDER = ROOT / "enrichment" / "business_intelligence_results"
LOG_FOLDER = ROOT / "enrichment" / "business_intelligence_logs"

QUEUE_FILE = BATCH_FOLDER / "business_intelligence_queue.csv"

BATCH_SIZE = 50

TARGET_FIELDS = [
    "primary_category",
    "primary_business_type",
    "business_types",
    "offerings_tags",
    "service_tags",
    "amenities_tags",
    "audience_tags",
    "ownership_tags",
    "service_model_tags",
    "searchable_keywords",
    "restaurant_intelligence_review_needed",
    "restaurant_intelligence_notes",
    "restaurant_intelligence_source",
    "restaurant_intelligence_updated_date",
]
