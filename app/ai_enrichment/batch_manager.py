import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.ai_enrichment.config import BATCH_FOLDER, RESULTS_FOLDER


def batch_status(batch_file):
    batch = pd.read_csv(batch_file, dtype=str)
    total = len(batch)

    result_file = RESULTS_FOLDER / batch_file.name.replace(".csv", "_results.csv")

    if result_file.exists():
        results = pd.read_csv(result_file, dtype=str)

        reviewed = (
            results["review_status"]
            .fillna("")
            .str.lower()
            .isin(["approved", "rejected", "skipped"])
            .sum()
        )

        ready = (
            results["ready_to_merge"]
            .fillna("")
            .str.lower()
            .eq("yes")
            .sum()
        )
    else:
        reviewed = 0
        ready = 0

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
        "ready": ready,
        "remaining": total - reviewed,
    }


def show_batches():
    print("=" * 70)
    print("203local AI Enrichment Batch Manager")
    print("=" * 70)

    batches = sorted(BATCH_FOLDER.glob("ai_batch_*.csv"))

    if not batches:
        print("No AI enrichment batches found.")
        return

    for batch in batches:
        info = batch_status(batch)

        print(
            f"{batch.name:<22}"
            f"{info['status']:<14}"
            f"Reviewed: {info['reviewed']:>3}/{info['total']:<3} "
            f"Ready: {info['ready']:>3} "
            f"Remaining: {info['remaining']:>3}"
        )

    print("=" * 70)


def find_current_batch():
    batches = sorted(BATCH_FOLDER.glob("ai_batch_*.csv"))

    for batch in batches:
        info = batch_status(batch)
        if info["status"] == "In Progress":
            return batch

    for batch in batches:
        info = batch_status(batch)
        if info["status"] == "Not Started":
            return batch

    return None


if __name__ == "__main__":
    show_batches()
