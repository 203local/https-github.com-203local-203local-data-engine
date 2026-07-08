import pandas as pd

from app.core.workbook import find_master_workbook, save_report_workbook
from app.orchestrator.queue import build_queue


def run(limit=25):
    workbook = find_master_workbook()

    if workbook is None:
        print("No master workbook found.")
        return

    df = pd.read_excel(workbook)
    queue = build_queue(df)

    repair_count = 0

    for _, row in queue.head(limit).iterrows():
        business_id = row.get("business_id")

        if pd.isna(business_id):
            continue

        mask = df["business_id"] == business_id

        # Safe placeholder write-back field.
        # This proves the write-back mechanism works without changing real data.
        df.loc[mask, "orchestrator_review_status"] = "Needs Repair Review"

        repair_count += 1

    output_path = save_report_workbook(
        df=df,
        source_path=workbook,
        suffix="orchestrator_writeback_preview",
    )

    print()
    print("=" * 70)
    print("Orchestrator Write-Back Preview Complete")
    print("=" * 70)
    print(f"Businesses marked for review: {repair_count}")
    print(f"Saved preview workbook to: {output_path}")
