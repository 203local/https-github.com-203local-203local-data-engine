from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

from config import MASTER_FILE, BACKUP_FOLDER, REPORT_FOLDER, EXPORT_FOLDER
from utils import is_blank

def count_missing(df, column):
    if column not in df.columns:
        return "Column missing"
    return int(df[column].apply(is_blank).sum())

def show_summary():
    print("=" * 60)
    print("203local Data Engine v2.0 Dashboard")
    print("=" * 60)

    df = pd.read_excel(MASTER_FILE)

    print(f"Businesses:        {len(df):,}")
    print(f"Fields:            {len(df.columns):,}")
    print()
    print("Data Gaps")
    print("-" * 60)
    print(f"Missing websites:  {count_missing(df, 'website'):,}")
    print(f"Missing emails:    {count_missing(df, 'email'):,}")
    print(f"Missing phones:    {count_missing(df, 'phone'):,}")
    print(f"Missing counties:  {count_missing(df, 'county'):,}")
    print()

    backups = sorted(BACKUP_FOLDER.glob('*.xlsx')) if BACKUP_FOLDER.exists() else []
    reports = sorted(REPORT_FOLDER.glob('*.xlsx')) if REPORT_FOLDER.exists() else []
    exports = sorted(EXPORT_FOLDER.glob('*.csv')) if EXPORT_FOLDER.exists() else []

    print("System Status")
    print("-" * 60)
    print(f"Backups:           {len(backups):,}")
    print(f"Reports:           {len(reports):,}")
    print(f"Exports:           {len(exports):,}")

    if backups:
        print(f"Latest backup:     {backups[-1].name}")
    if reports:
        print(f"Latest report:     {reports[-1].name}")
    if exports:
        print(f"Latest export:     {exports[-1].name}")

    print("=" * 60)

if __name__ == "__main__":
    show_summary()
