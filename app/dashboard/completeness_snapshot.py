import pandas as pd

from app.core.workbook import find_master_workbook
from app.completeness.analyzer import analyze


def run():
    workbook = find_master_workbook()

    if workbook is None:
        print("No master workbook found.")
        return

    df = pd.read_excel(workbook)

    business = input("Business name: ").strip()

    matches = df[
        df["post_title"]
        .fillna("")
        .str.contains(business, case=False, regex=False, na=False)
    ]

    if matches.empty:
        print("No match found.")
        return

    row = matches.iloc[0]
    result = analyze(row)

    print()
    print("=" * 60)
    print(row["post_title"])
    print("=" * 60)
    print(f"Town: {row.get('town', '')}")
    print(f"Completeness Score: {result.score}%")

    print()
    print("Missing Fields:")
    if result.missing_fields:
        for field in result.missing_fields:
            print(f"- {field}")
    else:
        print("- None")

    print()
    print("Suggested Repairs:")
    if result.suggested_repairs:
        for repair in result.suggested_repairs:
            print(f"- {repair}")
    else:
        print("- None")
