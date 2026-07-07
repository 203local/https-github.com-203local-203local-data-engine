from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(ROOT))

from app.jobs.website_discovery.config import BATCH_FOLDER, RESULTS_FOLDER

def batch_status(batch_file):
    batch = pd.read_csv(batch_file)
    result_file = RESULTS_FOLDER / batch_file.name.replace(".csv", "_interactive_results.csv")

    total = len(batch)

    if result_file.exists():
        results = pd.read_csv(result_file)
        completed = results["ready_to_merge"].astype(str).str.lower().eq("yes").sum()
        reviewed = results["review_status"].astype(str).str.lower().isin(
            ["website found", "skipped", "no website found"]
        ).sum()
    else:
        completed = 0
        reviewed = 0

    if reviewed == 0:
        status = "Not Started"
    elif reviewed < total:
        status = "In Progress"
    else:
        status = "Complete"

    return {
        "batch": batch_file.name,
        "total": total,
        "reviewed": reviewed,
        "completed": completed,
        "remaining": total - reviewed,
        "status": status,
        "result_file": result_file.name if result_file.exists() else "",
    }

def show_batches():
    print("=" * 70)
    print("203local Website Discovery Batch Manager")
    print("=" * 70)

    batches = sorted(BATCH_FOLDER.glob("website_batch_*.csv"))

    if not batches:
        print("No website batches found.")
        return

    rows = [batch_status(batch) for batch in batches]

    for row in rows:
        print(
            f'{row["batch"]:<28} '
            f'{row["status"]:<14} '
            f'Reviewed: {row["reviewed"]:>3}/{row["total"]:<3} '
            f'Ready: {row["completed"]:>3} '
            f'Remaining: {row["remaining"]:>3}'
        )

    print("=" * 70)

if __name__ == "__main__":
    show_batches()

    def find_current_batch():
    batches = sorted(BATCH_FOLDER.glob("website_batch_*.csv"))

    for batch in batches:
        status = batch_status(batch)
        if status["status"] == "In Progress":
            return batch

    for batch in batches:
        status = batch_status(batch)
        if status["status"] == "Not Started":
            return batch

    return None