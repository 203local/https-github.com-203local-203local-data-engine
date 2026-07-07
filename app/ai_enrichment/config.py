from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

BATCH_FOLDER = ROOT / "enrichment" / "ai_batches"
RESULTS_FOLDER = ROOT / "enrichment" / "ai_results"
LOG_FOLDER = ROOT / "enrichment" / "ai_logs"

QUEUE_FILE = BATCH_FOLDER / "ai_enrichment_queue.csv"
DEFAULT_BATCH_FILE = BATCH_FOLDER / "ai_batch_0001.csv"
DEFAULT_OUTPUT_FILE = RESULTS_FOLDER / "ai_batch_0001_results.csv"

BATCH_SIZE = 50

TARGET_FIELDS = [
    "post_content",
    "seo_directory_title",
    "seo_meta_description",
    "searchable_keywords",
    "restaurant_intelligence_notes",
    "restaurant_intelligence_source",
    "restaurant_intelligence_updated_date",
]
