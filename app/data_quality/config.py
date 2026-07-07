from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

REPORT_FOLDER = ROOT / "reports"

QUALITY_REPORT_FILE = REPORT_FOLDER / "Data_Quality_Report.csv"

CORE_FIELDS = [
    "business_id",
    "post_title",
    "town",
    "county",
    "phone",
    "website",
    "email",
    "primary_category",
    "primary_business_type",
    "post_content",
    "seo_directory_title",
    "seo_meta_description",
]
