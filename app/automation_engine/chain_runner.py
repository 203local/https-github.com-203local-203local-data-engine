from app.automation_engine.runner import run_job
from app.queue_manager.queue import get_next_batch


def run_chain(job_name, batches=3, limit=5):
    print("=" * 70)
    print("Automation Chain Runner")
    print("=" * 70)
    print("Job:", job_name)
    print("Max batches:", batches)
    print("Limit per batch:", limit)

    completed = 0

    for _ in range(batches):
        next_batch = get_next_batch(job_name)

        if next_batch is None:
            print("No unfinished batches found.")
            break

        print()
        print("-" * 70)
        print("Next batch:", next_batch.name)
        print("-" * 70)

        run_job(job_name, limit=limit)
        completed += 1

    print("=" * 70)
    print("Chain complete")
    print("Batches attempted:", completed)


def show_menu():
    print("=" * 70)
    print("203local Automation Chain Runner")
    print("=" * 70)
    print("1. AI Enrichment")
    print("2. Restaurant Intelligence")
    print("3. Business Intelligence")
    print("4. Exit")

    choice = input("Select a job: ").strip()

    job_map = {
        "1": "ai_enrichment",
        "2": "restaurant_intelligence",
        "3": "business_intelligence",
    }

    if choice == "4":
        print("Goodbye.")
        return

    job_name = job_map.get(choice)

    if not job_name:
        print("Invalid choice.")
        return

    batches = input("Max batches [3]: ").strip()
    batches = int(batches) if batches else 3

    limit = input("Limit per batch [5]: ").strip()
    limit = int(limit) if limit else 5

    run_chain(job_name, batches=batches, limit=limit)


if __name__ == "__main__":
    show_menu()
