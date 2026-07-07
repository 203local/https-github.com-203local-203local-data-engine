from app.automation_engine.runner import run_job
from app.playbooks.playbooks import PLAYBOOKS


def list_playbooks():
    return sorted(PLAYBOOKS.keys())


def run_playbook(playbook_key, limit=5):
    playbook = PLAYBOOKS.get(playbook_key)

    if playbook is None:
        print("Unknown playbook:", playbook_key)
        print("Available playbooks:", ", ".join(list_playbooks()))
        return

    print("=" * 70)
    print("203local Playbook Runner")
    print("=" * 70)
    print("Playbook:", playbook["name"])
    print("Limit per job:", limit)

    for job_name in playbook["jobs"]:
        print()
        print("-" * 70)
        print("Running:", job_name)
        print("-" * 70)

        run_job(job_name, limit=limit)

    print("=" * 70)
    print("Playbook complete:", playbook["name"])


def show_menu():
    keys = list_playbooks()

    print("=" * 70)
    print("203local Playbooks")
    print("=" * 70)

    for i, key in enumerate(keys, start=1):
        print(f"{i}. {PLAYBOOKS[key]['name']}")

    print(f"{len(keys) + 1}. Exit")

    choice = input("Select a playbook: ").strip()

    if choice == str(len(keys) + 1):
        print("Goodbye.")
        return

    try:
        playbook_key = keys[int(choice) - 1]
    except Exception:
        print("Invalid choice.")
        return

    limit = input("Limit per job [5]: ").strip()
    limit = int(limit) if limit else 5

    run_playbook(playbook_key, limit=limit)


if __name__ == "__main__":
    show_menu()
