from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

BATCH_FOLDER = ROOT / "enrichment" / "email_batches"
RESULTS_FOLDER = ROOT / "enrichment" / "email_results"
LOG_FOLDER = ROOT / "enrichment" / "email_logs"

DEFAULT_BATCH_FILE = BATCH_FOLDER / "email_batch_0001.csv"
DEFAULT_OUTPUT_FILE = RESULTS_FOLDER / "email_batch_0001_interactive_results.csv"

DEFAULT_REVIEW_STATUS = "Needs Review"
READY_TO_MERGE_DEFAULT = "No"
