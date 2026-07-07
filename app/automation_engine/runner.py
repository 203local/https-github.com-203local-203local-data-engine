import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.automation_engine.config import DEFAULT_JOB_LIMIT
from app.automation_engine.jobs import list_jobs, get_job
from app.automation_engine.state import record_run
from app.queue_manager.queue import get_next_batch
from app.queue_manager.state import update_queue_status


def run_job(job_name, limit=DEFAULT_JOB_LIMIT):
    job = get_job(job_name)

    if job is None:
        print("Unknown job:", job_name)
        print("Available jobs:", ", ".join(list_jobs()))
        return

    print("=" * 70)
    print("Automation Engine")
    print("=" * 70)
    print("Running job:", job_name)
    print("Limit:", limit)

    next_batch = get_next_batch(job_name)
    batch_name = next_batch.name if next_batch else "unknown"

    if next_batch:
        print("Queue batch:", batch_name)
        update_queue_status(job_name, batch_name, "In Progress", {"limit": limit})

    try:
        job(limit=limit)

        if next_batch:
            update_queue_status(job_name, batch_name, "Complete", {"limit": limit})

        record_run(job_name, "Complete", {"limit": limit, "batch": batch_name})
        print("✓ Job complete")
    except Exception as e:
        if next_batch:
            update_queue_status(job_name, batch_name, "Failed", {"limit": limit, "error": str(e)})

        record_run(job_name, "Failed", {"limit": limit, "batch": batch_name, "error": str(e)})
        print("✗ Job failed:", e)


def show_menu():
    jobs = list_jobs()

    print("=" * 70)
    print("203local Automation Engine")
    print("=" * 70)

    for i, job in enumerate(jobs, start=1):
        print(f"{i}. {job}")

    print(f"{len(jobs) + 1}. Exit")

    choice = input("Select a job: ").strip()

    if choice == str(len(jobs) + 1):
        print("Goodbye.")
        return

    try:
        index = int(choice) - 1
        job_name = jobs[index]
    except Exception:
        print("Invalid choice.")
        return

    limit = input(f"Limit [{DEFAULT_JOB_LIMIT}]: ").strip()
    limit = int(limit) if limit else DEFAULT_JOB_LIMIT

    run_job(job_name, limit=limit)


if __name__ == "__main__":
    show_menu()
