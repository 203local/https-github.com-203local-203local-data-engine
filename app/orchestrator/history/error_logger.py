from datetime import datetime
import csv
from pathlib import Path


ERROR_LOG_FILE = Path("logs/enrichment_errors.csv")


def log_error(error):
    ERROR_LOG_FILE.parent.mkdir(exist_ok=True)

    file_exists = ERROR_LOG_FILE.exists()

    with ERROR_LOG_FILE.open("a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "worker",
                "business_id",
                "business_name",
                "town",
                "error",
                "traceback",
            ])

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            error.get("worker"),
            error.get("business_id"),
            error.get("business_name"),
            error.get("town"),
            error.get("error"),
            error.get("traceback"),
        ])
