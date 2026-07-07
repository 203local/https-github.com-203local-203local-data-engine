from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent

BATCH_FOLDER = ROOT / "enrichment" / "batches"
RESULTS_FOLDER = ROOT / "enrichment" / "results"
LOG_FOLDER = ROOT / "enrichment" / "logs"

DEFAULT_BATCH_FILE = BATCH_FOLDER / "website_batch_0001.csv"
DEFAULT_OUTPUT_FILE = RESULTS_FOLDER / "website_batch_0001_discovery_results.csv"

CONFIDENCE_HIGH = 90
CONFIDENCE_MEDIUM = 70
CONFIDENCE_LOW = 50

DEFAULT_REVIEW_STATUS = "Needs Review"
READY_TO_MERGE_DEFAULT = "No"

SEARCH_LIMIT_PER_BUSINESS = 5