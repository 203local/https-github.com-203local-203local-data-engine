from pathlib import Path
import shutil
import pandas as pd
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from config import MASTER_FILE, BACKUP_FOLDER
from utils import timestamp

def backup_master():
    BACKUP_FOLDER.mkdir(exist_ok=True)
    if not MASTER_FILE.exists():
        print("Master not found:", MASTER_FILE)
        raise SystemExit(1)
    backup_path = BACKUP_FOLDER / f"203local_Master_Backup_{timestamp()}.xlsx"
    shutil.copy2(MASTER_FILE, backup_path)
    return backup_path

def load_master(create_backup=True):
    if not MASTER_FILE.exists():
        print("Master not found:", MASTER_FILE)
        print("Put your spreadsheet here and rename it exactly:")
        print(MASTER_FILE)
        raise SystemExit(1)

    if create_backup:
        backup = backup_master()
        print("Backup created:", backup)

    df = pd.read_excel(MASTER_FILE)
    print(f"Loaded {len(df):,} rows and {len(df.columns)} columns.")
    return df

if __name__ == "__main__":
    load_master(create_backup=True)
