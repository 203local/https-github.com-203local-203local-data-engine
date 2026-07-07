from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.jobs.website_discovery.discovery_config import (
    BATCH_FOLDER,
    RESULTS_FOLDER,
)


def batch_status(batch_file):
    batch = pd.read_csv(batch_file)
    total = len(batch)

    result_file = RESULTS_FOLDER / batch_file.name.replace(
        ".csv",
        "_interactive_results.csv",
    )

    if result_file.exists():
        results = pd.read_csv(result_file)

        reviewed = (
            results["review_status"]
            .fillna("")
            .astype(str)
            .str.lower()
            .isin(["website found", "skipped", "no website found"])
            .sum()
        )

        completed = (
            results["ready_to_merge"]
            .fillna("")
            .astype(str)
            .str.lower()
            .eq("yes")
            .sum()
        )

    else:
        reviewed = 0
        completed = 0

    if reviewed == 0:
        status = "Not Started"
    elif reviewed < total:
        status = "In Progress"
    else:
        status = "Complete"

    return {
        "batch": batch_file,
        "status": status,
        "total": total,
        "reviewed": reviewed,
        "completed": completed,
        "remaining": total - reviewed,
    }


def show_batches():
    print("=" * 70)
    print("203local Website Discovery Batch Manager")
    print("=" * 70)

    batches = sorted(BATCH_FOLDER.glob("website_batch_*.csv"))

    if not batches:
        print("No website batches found.")
        return

    for batch in batches:
        info = batch_status(batch)

        print(
            f"{batch.name:<28}"
            f"{info['status']:<14}"
            f"Reviewed: {info['reviewed']:>3}/{info['total']:<3} "
            f"Ready: {info['completed']:>3} "
            f"Remaining: {info['remaining']:>3}"
        )

    print("=" * 70)


def find_current_batch():
    batches = sorted(BATCH_FOLDER.glob("website_batch_*.csv"))

    # Resume an in-progress batch first
    for batch in batches:
        info = batch_status(batch)
        if info["status"] == "In Progress":
            return batch

    # Otherwise start the first new batch
    for batch in batches:
        info = batch_status(batch)
        if info["status"] == "Not Started":
            return batch

    return None


if __name__ == "__main__":
    show_batches()
    