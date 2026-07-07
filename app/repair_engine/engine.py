import pandas as pd
from pathlib import Path

from app.repair_engine.seo.repair import run as run_seo_repair


MASTER_DIR = Path("master")


def find_latest_master():
    files = list(MASTER_DIR.glob("203local_Master_Directory*.xlsx"))

    if not files:
        return None

    ignored_tags = [
        "_seo_repaired",
        "_website_repaired",
        "_phone_repaired",
        "_email_repaired",
        "_social_repaired",
        "_hours_repaired",
        "_images_repaired",
    ]

    files = [
        f for f in files
        if not f.name.startswith("~$")
        and not any(tag in f.name for tag in ignored_tags)
    ]
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    return files[0]


def run_seo_repair_workflow():
    print("\n=== SEO Auto-Fix ===")

    master_path = find_latest_master()

    if master_path is None:
        print("No master directory workbook found in the data folder.")
        return

    print(f"Using master file: {master_path}")

    df = pd.read_excel(master_path)

    df, report = run_seo_repair(df)

    output_path = Path("reports") / (master_path.stem + "_seo_repaired.xlsx")

    df.to_excel(output_path, index=False)

    report.print_summary()

    print("\nSaved repaired file to:")
    print(output_path)
