import pandas as pd

from app.core.workbook import find_master_workbook
from app.orchestrator.executor import execute


def run(limit=25):
    workbook = find_master_workbook()

    if workbook is None:
        print("No master workbook found.")
        return

    df = pd.read_excel(workbook)

    total = min(limit, len(df))

    print()
    print("=" * 70)
    print("203local Batch Repair Orchestrator")
    print("=" * 70)
    print(f"Workbook: {workbook}")
    print(f"Processing first {total} businesses")
    print("=" * 70)

    processed = 0
    planned_steps = 0

    for index, row in df.head(limit).iterrows():
        result = execute(row)

        processed += 1
        planned_steps += len(result.steps)

        print()
        print("-" * 70)
        print(f"{processed}/{total}: {result.business_name}")
        print(f"Current Score: {result.current_score}%")
        print(f"Estimated After: {result.estimated_score_after}%")

        if result.executed_steps:
            print("Executed Steps:")
            for step in result.executed_steps:
                print(f"✓ {step}")
        else:
            print("No repair steps needed.")

    print()
    print("=" * 70)
    print("Batch Repair Complete")
    print("=" * 70)
    print(f"Businesses processed: {processed}")
    print(f"Planned/executed steps: {planned_steps}")
