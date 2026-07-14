from pathlib import Path
from datetime import datetime
import shutil


MASTER_FILE = Path("master/203local_Master_Directory.xlsx")
BACKUP_DIR = Path("master/backups")


def create_backup():
    """
    Creates a timestamped backup of the master workbook.

    Returns:
        Path to the backup file.
    """

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

    backup_path = (
        BACKUP_DIR
        / f"203local_Master_Directory_{timestamp}.xlsx"
    )

    shutil.copy2(
        MASTER_FILE,
        backup_path,
    )

    return backup_path
