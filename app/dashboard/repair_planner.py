import pandas as pd

from app.core.workbook import find_master_workbook
from app.completeness.planner import build_plan


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

    plan = build_plan(row)

    print()
    print("=" * 65)
    print(row["post_title"])
    print("=" * 65)
    print(f"Current Score: {plan.current_score}%")
    print(f"Estimated After Repairs: {plan.estimated_score_after}%")

    print()
    print("Missing Fields")
    print("-" * 30)

    if plan.missing_fields:
        for field in plan.missing_fields:
            print(f"• {field}")
    else:
        print("None")

    print()
    print("Recommended Repair Order")
    print("-" * 30)

    if plan.steps:
        for i, step in enumerate(plan.steps, start=1):
            print(f"{i}. {step}")
    else:
        print("Nothing to repair.")
