import csv
from datetime import datetime
from pathlib import Path


DEFAULT_LOG_FILE = Path("logs/master_change_log.csv")

FIELDNAMES = [
    "timestamp",
    "business_id",
    "business_name",
    "field",
    "old_value",
    "new_value",
    "source",
    "confidence",
]


def append_changes(
    changes,
    log_file=DEFAULT_LOG_FILE,
):
    log_file = Path(log_file)
    log_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_exists = log_file.exists()

    with log_file.open(
        "a",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=FIELDNAMES,
        )

        if not file_exists:
            writer.writeheader()

        timestamp = datetime.now().isoformat(
            timespec="seconds"
        )

        for change in changes:
            writer.writerow(
                {
                    "timestamp": timestamp,
                    "business_id": change.get(
                        "business_id",
                        "",
                    ),
                    "business_name": change.get(
                        "business_name",
                        "",
                    ),
                    "field": change.get(
                        "field",
                        "",
                    ),
                    "old_value": change.get(
                        "old_value",
                        "",
                    ),
                    "new_value": change.get(
                        "new_value",
                        "",
                    ),
                    "source": change.get(
                        "source",
                        "",
                    ),
                    "confidence": change.get(
                        "confidence",
                        "",
                    ),
                }
            )

    return len(changes)
