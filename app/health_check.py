from pathlib import Path
import importlib
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def check_path(label, path):
    if path.exists():
        print(f"✓ {label}: {path}")
        return True
    print(f"✗ {label} missing: {path}")
    return False


def check_import(module_name):
    try:
        importlib.import_module(module_name)
        print(f"✓ Import: {module_name}")
        return True
    except Exception as e:
        print(f"✗ Import failed: {module_name}")
        print(f"  {e}")
        return False


def run_health_check():
    print("=" * 60)
    print("203local Data Engine Health Check")
    print("=" * 60)

    paths = [
        ("Master workbook", ROOT / "master" / "203local_Master_Directory.xlsx"),
        ("Backups folder", ROOT / "backups"),
        ("Reports folder", ROOT / "reports"),
        ("Exports folder", ROOT / "exports"),
        ("Enrichment folder", ROOT / "enrichment"),
        ("Website batches", ROOT / "enrichment" / "batches"),
        ("Website results", ROOT / "enrichment" / "results"),
        ("Reference folder", ROOT / "reference"),
        ("Taxonomy folder", ROOT / "taxonomy"),
    ]

    path_results = [check_path(label, path) for label, path in paths]

    print()
    print("Module Imports")
    print("-" * 60)

    modules = [
        "config",
        "utils",
        "app.dashboard.summary",
        "app.jobs.website_discovery.interactive",
        "app.jobs.website_discovery.batch_manager",
        "app.jobs.website_discovery.merge_preview",
        "scripts.master_loader",
        "scripts.validator",
        "scripts.website_export",
        "scripts.generic_merge_manager",
    ]

    import_results = [check_import(module) for module in modules]

    print()
    print("=" * 60)

    if all(path_results) and all(import_results):
        print("System status: HEALTHY")
    else:
        print("System status: NEEDS ATTENTION")

    print("=" * 60)


if __name__ == "__main__":
    run_health_check()

    