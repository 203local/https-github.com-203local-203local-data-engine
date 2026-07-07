from app.dashboard.summary import show_summary
from app.jobs.website_discovery.interactive import run as run_website_discovery
from app.jobs.website_discovery.batch_manager import show_batches, find_current_batch


def continue_website_discovery():
    batch = find_current_batch()

    if batch is None:
        print("No website discovery batches found.")
        return

    print()
    print("Continuing Website Discovery")
    print("Batch:", batch.name)
    print()

    run_website_discovery()


def menu():
    while True:
        print()
        print("=" * 60)
        print("203local Data Engine v2.2")
        print("=" * 60)
        print("1. Dashboard")
        print("2. Continue Website Discovery")
        print("3. Interactive Website Discovery")
        print("4. Website Batch Manager")
        print("5. Exit")
        print()

        choice = input("Select an option: ").strip()

        if choice == "1":
            show_summary()
        elif choice == "2":
            continue_website_discovery()
        elif choice == "3":
            run_website_discovery()
        elif choice == "4":
            show_batches()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    menu()