import pandas as pd

from app.core.workbook import find_master_workbook
from app.orchestrator.engine import run_business


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

    result = run_business(row)

    print()
    print("=" * 70)
    print(result.business_name)
    print("=" * 70)
    print(f"Current Score: {result.current_score}%")
    print(f"Estimated Score After Repairs: {result.estimated_score_after}%")

    print()
    print("Repair Plan")
    print("-" * 30)

    if result.steps:
        for i, step in enumerate(result.steps, 1):
            print(f"{i}. {step}")
    else:
        print("Nothing to repair.")

    print()
    print("Execution Status")
    print("-" * 30)

    if result.executed_steps:
        for step in result.executed_steps:
            print(f"✓ {step}")

    if result.skipped_steps:
        for step in result.skipped_steps:
            print(f"○ {step} (planned)")
