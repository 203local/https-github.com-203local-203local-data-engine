from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_NAME = "203local Data Engine"

MASTER_FILE = ROOT / "master" / "203local_Master_Directory.xlsx"
BACKUP_FOLDER = ROOT / "backups"
EXPORT_FOLDER = ROOT / "exports"
REPORT_FOLDER = ROOT / "reports"
LOG_FOLDER = ROOT / "logs"
TAXONOMY_FOLDER = ROOT / "taxonomy"

FIELD_DICTIONARY_FILE = TAXONOMY_FOLDER / "field_dictionary.xlsx"

# Fallback required columns if the field dictionary is missing
REQUIRED_COLUMNS = [
    "business_id",
    "post_title",
    "town",
    "county",
    "phone",
    "website",
    "email",
    "primary_category",
    "primary_business_type",
]

TEMP_FOLDER = ROOT / "cache"

