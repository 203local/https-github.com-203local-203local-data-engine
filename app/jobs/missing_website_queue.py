from pathlib import Path

import pandas as pd

MASTER_FILE = Path("master/203local_Master_Directory.xlsx")
OUTPUT_FILE = Path("enrichment/missing_website_queue.csv")


def clean(series):
    return (
        series.fillna("")
        .astype(str)
        .str.strip()
    )


def build_queue():
    xls = pd.ExcelFile(MASTER_FILE)
    sheet = xls.sheet_names[0]

    df = pd.read_excel(
        MASTER_FILE,
        sheet_name=sheet,
    )

    website = clean(df["website"])

    queue = df.loc[website.eq("")].copy()

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    queue.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print()
    print("=" * 60)
    print("Missing Website Queue")
    print("=" * 60)
    print(f"Worksheet: {sheet}")
    print(f"Businesses: {len(queue):,}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_queue()
