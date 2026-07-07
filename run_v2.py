from app.dashboard.summary import show_summary
from app.jobs.website_discovery import run as run_website_discovery

def menu():
    print()
    print("=" * 60)
    print("203local Data Engine v2.0")
    print("=" * 60)
    print("1. Dashboard")
    print("2. Website Discovery Job")
    print("3. Exit")
    print()

    choice = input("Select an option: ").strip()

    if choice == "1":
        show_summary()
    elif choice == "2":
        run_website_discovery()
    elif choice == "3":
        print("Goodbye.")
    else:
        print("Invalid option.")

if __name__ == "__main__":
    menu()
