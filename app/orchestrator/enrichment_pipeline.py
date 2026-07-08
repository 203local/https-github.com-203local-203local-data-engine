import pandas as pd

from app.core.workbook import find_master_workbook, save_report_workbook
from app.merge.merge_engine import merge_updates
from app.merge.apply_updates import apply_updates
from app.orchestrator.queue import build_queue
from app.workers.default_registry import registry
from app.workers.safe_runner import run_worker
from app.orchestrator.history.state_manager import save_state
from app.orchestrator.history.error_logger import log_error


def run(limit=25):
    workbook = find_master_workbook()

    if workbook is None:
        print("No master workbook found.")
        return

    df = pd.read_excel(workbook)
    queue = build_queue(df).head(limit)

    total_updates = 0
    accepted = 0
    rejected = 0
    applied = 0

    print()
    print("=" * 70)
    print("203local Enrichment Pipeline")
    print("=" * 70)
    print(f"Businesses selected: {len(queue)}")

    for i, (_, row) in enumerate(queue.iterrows(), start=1):
        print()
        print("-" * 70)
        print(f"{i}/{len(queue)}: {row.get('post_title')} ({row.get('town')})")

        business_id = row.get("business_id")

        for worker in registry.runnable(row):
            print(f"  Running: {worker.name}")

            result, error = run_worker(worker, row)

            if error:
                print(f"    ERROR: {error['error']}")
                log_error(error)
                continue

            total_updates += len(result.updates)

            merge_result = merge_updates(row, result.updates)

            accepted += len(merge_result.accepted_updates)
            rejected += len(merge_result.rejected_updates)

            if pd.notna(business_id):
                applied += apply_updates(
                    df,
                    business_id,
                    merge_result.accepted_updates,
                )

            print(f"    Accepted: {len(merge_result.accepted_updates)}")
            print(f"    Rejected: {len(merge_result.rejected_updates)}")

        save_state(
            last_business_id=business_id,
            completed=i,
        )

    output_path = save_report_workbook(
        df=df,
        source_path=workbook,
        suffix="enrichment_pipeline_preview",
    )

    print()
    print("=" * 70)
    print("Enrichment Pipeline Complete")
    print("=" * 70)
    print(f"Worker updates produced: {total_updates}")
    print(f"Updates accepted: {accepted}")
    print(f"Updates rejected: {rejected}")
    print(f"Updates applied to preview: {applied}")
    print(f"Saved preview workbook to: {output_path}")
