from scripts.master_loader import load_master
from scripts.validator import run_validation

def menu():
    print("=" * 50)
    print("203local Data Engine")
    print("=" * 50)
    print("1. Load + Backup Master")
    print("2. Validate Master Spreadsheet")
    print("3. Exit")
    print()

    choice = input("Select an option: ").strip()

    if choice == "1":
        load_master(create_backup=True)
    elif choice == "2":
        run_validation()
    elif choice == "3":
        print("Goodbye.")
    else:
        print("Invalid option.")

if __name__ == "__main__":
    menu()
