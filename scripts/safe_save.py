from pathlib import Path
import os
import shutil
import pandas as pd
from utils import timestamp

def safe_write_excel(df, target_path, backup_folder, temp_folder):
    target_path = Path(target_path)
    backup_folder = Path(backup_folder)
    temp_folder = Path(temp_folder)

    backup_folder.mkdir(exist_ok=True)
    temp_folder.mkdir(exist_ok=True)

    backup_path = backup_folder / f"{target_path.stem}_Backup_{timestamp()}{target_path.suffix}"
    shutil.copy2(target_path, backup_path)

    temp_path = temp_folder / f"{target_path.stem}_NEW_{timestamp()}{target_path.suffix}"

    df.to_excel(temp_path, index=False)

    test_df = pd.read_excel(temp_path, nrows=5)

    if not temp_path.exists() or temp_path.stat().st_size == 0:
        raise RuntimeError("Safe save failed.")

    os.replace(temp_path, target_path)

    return {
        "target_path": str(target_path),
        "backup_path": str(backup_path),
        "verified_rows_sampled": len(test_df),
    }
