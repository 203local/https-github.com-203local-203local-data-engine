from scripts.master_loader import load_master
from scripts.validator import run_validation
from scripts.dashboard import show_dashboard
from scripts.website_export import export_website_csv

print("=" * 50)
print("203local Data Engine")
print("=" * 50)
print("1. Dashboard")
print("2. Load + Backup Master")
print("3. Validate Master Spreadsheet")
print("4. Export Website CSV")
print("5. Exit")
print()

choice = input("Select an option: ")

if choice == "1":
    show_dashboard()
elif choice == "2":
    load_master(create_backup=True)
elif choice == "3":
    run_validation()
elif choice == "4":
    export_website_csv()
elif choice == "5":
    print("Goodbye.")
else:
    print("Invalid option.")
