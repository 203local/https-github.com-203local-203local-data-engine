import pandas as pd

from app.core.workbook import find_master_workbook, save_report_workbook
from app.merge.merge_engine import merge_updates
from app.merge.apply_updates import apply_updates
from app.workers.google_business_worker import GoogleBusinessWorker


def run(limit=25):
    workbook = find_master_workbook()

    if workbook is None:
        print("No master workbook found.")
        return

    df = pd.read_excel(workbook)

    worker = GoogleBusinessWorker()

    total_updates = 0
    accepted = 0
    rejected = 0
    applied = 0

    for _, row in df.head(limit).iterrows():
        if not worker.can_run(row):
            continue

        worker_result = worker.run(row)
        merge_result = merge_updates(row, worker_result.updates)

        total_updates += len(worker_result.updates)
        accepted += len(merge_result.accepted_updates)
        rejected += len(merge_result.rejected_updates)

        business_id = row.get("business_id")
        if pd.notna(business_id):
            applied += apply_updates(
                df,
                business_id,
                merge_result.accepted_updates,
            )

    output_path = save_report_workbook(
        df=df,
        source_path=workbook,
        suffix="merge_preview",
    )

    print()
    print("=" * 70)
    print("Merge Preview Complete")
    print("=" * 70)
    print(f"Businesses scanned: {limit}")
    print(f"Worker updates produced: {total_updates}")
    print(f"Updates accepted: {accepted}")
    print(f"Updates rejected: {rejected}")
    print(f"Updates applied to preview: {applied}")
    print(f"Saved preview workbook to: {output_path}")
