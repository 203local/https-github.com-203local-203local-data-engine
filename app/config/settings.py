from pathlib import Path


# Workbook folders
MASTER_DIR = Path("master")
REPORTS_DIR = Path("reports")
BACKUPS_DIR = Path("backups")
LOGS_DIR = Path("logs")


# Default processing settings
DEFAULT_BATCH_LIMIT = 25
DEFAULT_HEALTH_SCORE_THRESHOLD = 90


# Merge settings
DEFAULT_MIN_CONFIDENCE = 0.75


# Report filenames / suffixes
MERGE_PREVIEW_SUFFIX = "merge_preview"
ORCHESTRATOR_WRITEBACK_PREVIEW_SUFFIX = "orchestrator_writeback_preview"
REPAIR_PIPELINE_SUFFIX = "repair_pipeline"


# Repair history
REPAIR_HISTORY_FILE = LOGS_DIR / "repair_history.csv"
