from datetime import datetime
import csv

from app.config.settings import REPAIR_HISTORY_FILE


HISTORY_FILE = REPAIR_HISTORY_FILE


def log_repair(business_name, repair_step, status="planned"):
    HISTORY_FILE.parent.mkdir(exist_ok=True)

    file_exists = HISTORY_FILE.exists()

    with HISTORY_FILE.open("a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "business_name",
                "repair_step",
                "status",
            ])

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            business_name,
            repair_step,
            status,
        ])
