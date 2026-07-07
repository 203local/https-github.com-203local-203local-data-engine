from app.dashboard.summary import show_summary

from app.jobs.website_discovery.interactive import run as run_website_discovery
from app.jobs.website_discovery.batch_manager import (
    show_batches as show_website_batches,
    find_current_batch as find_current_website_batch,
)
from app.jobs.website_discovery.merge_preview import show_merge_preview as show_website_merge_preview

from app.email_discovery.interactive import run as run_email_discovery
from app.email_discovery.batch_manager import (
    show_batches as show_email_batches,
    find_current_batch as find_current_email_batch,
)
from app.email_discovery.merge_preview import show_merge_preview as show_email_merge_preview
from app.email_discovery.merge import merge_emails


def continue_website_discovery():
    batch = find_current_website_batch()

    if batch is None:
        print("No website discovery batches found.")
        return

    print()
    print("Continuing Website Discovery")
    print("Batch:", batch.name)
    print()

    run_website_discovery()


def continue_email_discovery():
    batch = find_current_email_batch()

    if batch is None:
        print("No email discovery batches found.")
        return

    print()
    print("Continuing Email Discovery")
    print("Batch:", batch.name)
    print()

    run_email_discovery()


def menu():
    while True:
        print()
        print("=" * 60)
        print("203local Data Engine v2.2")
        print("=" * 60)
        print("1. Dashboard")
        print("2. Continue Website Discovery")
        print("3. Website Batch Manager")
        print("4. Website Merge Preview")
        print("5. Continue Email Discovery")
        print("6. Email Batch Manager")
        print("7. Email Merge Preview")
        print("8. Email Merge Manager")
        print("9. Exit")
        print()

        choice = input("Select an option: ").strip()

        if choice == "1":
            show_summary()
        elif choice == "2":
            continue_website_discovery()
        elif choice == "3":
            show_website_batches()
        elif choice == "4":
            show_website_merge_preview()
        elif choice == "5":
            continue_email_discovery()
        elif choice == "6":
            show_email_batches()
        elif choice == "7":
            show_email_merge_preview()
        elif choice == "8":
            merge_emails()
        elif choice == "9":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    menu()
