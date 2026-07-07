import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.automation_engine.config import DEFAULT_JOB_LIMIT
from app.automation_engine.jobs import list_jobs, get_job
from app.automation_engine.state import record_run


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

    try:
        job(limit=limit)
        record_run(job_name, "Complete", {"limit": limit})
        print("✓ Job complete")
    except Exception as e:
        record_run(job_name, "Failed", {"error": str(e)})
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
