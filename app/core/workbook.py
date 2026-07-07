from pathlib import Path
from datetime import datetime
import shutil
import pandas as pd


MASTER_DIR = Path("master")
REPORTS_DIR = Path("reports")
BACKUPS_DIR = Path("backups")


IGNORED_MASTER_TAGS = [
    "_seo_repaired",
    "_website_repaired",
    "_phone_repaired",
    "_email_repaired",
    "_social_repaired",
    "_hours_repaired",
    "_images_repaired",
]


def find_master_workbook():
    files = list(MASTER_DIR.glob("203local_Master_Directory*.xlsx"))

    files = [
        f for f in files
        if not f.name.startswith("~$")
        and not any(tag in f.name for tag in IGNORED_MASTER_TAGS)
    ]

    if not files:
        return None

    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return files[0]


def load_master_dataframe():
    master_path = find_master_workbook()

    if master_path is None:
        raise FileNotFoundError("No master directory workbook found.")

    df = pd.read_excel(master_path)
    return master_path, df


def save_report_workbook(df, source_path, suffix):
    REPORTS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = REPORTS_DIR / f"{source_path.stem}_{suffix}_{timestamp}.xlsx"

    df.to_excel(output_path, index=False)

    return output_path


def backup_master(source_path, label="Repair"):
    BACKUPS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUPS_DIR / f"{source_path.stem}_{label}_Backup_{timestamp}.xlsx"

    shutil.copy2(source_path, backup_path)

    return backup_path
