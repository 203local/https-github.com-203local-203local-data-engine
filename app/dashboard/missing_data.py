import pandas as pd

from app.core.workbook import find_master_workbook


def run():
    workbook = find_master_workbook()

    if workbook is None:
        print("No master workbook found.")
        return

    df = pd.read_excel(workbook)

    total = len(df)

    print()
    print("=" * 70)
    print("203local Missing Data Dashboard")
    print("=" * 70)
    print(f"Businesses: {total:,}")
    print()

    results = []

    for column in df.columns:
        missing = (
            df[column]
            .fillna("")
            .astype(str)
            .str.strip()
            .eq("")
            .sum()
        )

        complete = total - missing
        percent = (complete / total) * 100 if total else 0

        results.append(
            {
                "field": column,
                "missing": missing,
                "complete": complete,
                "percent": percent,
            }
        )

    results.sort(key=lambda r: r["missing"], reverse=True)

    print("Top 15 Fields Needing Attention")
    print("-" * 70)

    for row in results[:15]:
        print(
            f"{row['field'][:35]:35}"
            f"{row['missing']:>8} missing"
            f"   {row['percent']:6.1f}% complete"
        )

    print("-" * 70)
