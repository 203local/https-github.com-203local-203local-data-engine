from pathlib import Path
from time import monotonic
import json

import pandas as pd

from app.core.workbook import find_master_workbook, save_report_workbook
from app.merge.apply_updates import apply_updates
from app.merge.merge_engine import merge_updates
from app.workers.website_worker import WebsiteWorker


QUEUE_FILE = Path("enrichment/website_crawl_queue.csv")
CHECKPOINT_FILE = Path("enrichment/website_crawl_checkpoint.json")
CHECKPOINT_EVERY = 25
PROGRESS_EVERY = 10


def format_duration(seconds):
    seconds = max(0, int(seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours:
        return f"{hours}h {minutes}m {seconds}s"
    if minutes:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"


def load_processed_ids():
    if not CHECKPOINT_FILE.exists():
        return set()

    try:
        data = json.loads(CHECKPOINT_FILE.read_text())
        return {
            str(value)
            for value in data.get("processed_business_ids", [])
        }
    except (json.JSONDecodeError, OSError):
        return set()


def save_checkpoint(processed_ids):
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_FILE.write_text(
        json.dumps(
            {
                "processed_business_ids": sorted(processed_ids),
            },
            indent=2,
        )
    )


def run(limit=None):
    workbook = find_master_workbook()

    if workbook is None:
        print("No master workbook found.")
        return

    if not QUEUE_FILE.exists():
        print(f"Queue not found: {QUEUE_FILE}")
        return

    df = pd.read_excel(workbook)
    queue = pd.read_csv(QUEUE_FILE)

    required = {
        "business_id",
        "post_title",
        "town",
        "street",
        "website",
    }

    missing = required.difference(queue.columns)

    if missing:
        raise ValueError(
            "Queue is missing required columns: "
            + ", ".join(sorted(missing))
        )

    queue["business_id"] = queue["business_id"].astype(str)
    processed_ids = load_processed_ids()

    remaining = queue[
        ~queue["business_id"].isin(processed_ids)
    ].copy()

    if limit is not None:
        remaining = remaining.head(limit)

    total = len(remaining)

    if total == 0:
        print("No unprocessed businesses remain in the queue.")
        return

    worker = WebsiteWorker()

    accepted = 0
    rejected = 0
    applied = 0
    errors = 0
    started = monotonic()

    print()
    print("=" * 70)
    print("Free Website Crawl")
    print("=" * 70)
    print(f"Businesses remaining: {total:,}")
    print("Paid discovery: disabled")
    print("AI credits: $0")
    print()

    try:
        for position, (_, row) in enumerate(
            remaining.iterrows(),
            start=1,
        ):
            business_id = str(row.get("business_id", "")).strip()
            business_name = str(row.get("post_title", "")).strip()
            town = str(row.get("town", "")).strip()

            try:
                result = worker.run(row)
                merge_result = merge_updates(row, result.updates)

                accepted += len(merge_result.accepted_updates)
                rejected += len(merge_result.rejected_updates)

                applied += apply_updates(
                    df,
                    row.get("business_id"),
                    merge_result.accepted_updates,
                )

            except Exception as error:
                errors += 1
                print(
                    f"Warning: skipped {business_name} "
                    f"after {type(error).__name__}: {error}"
                )

            processed_ids.add(business_id)

            if (
                position % CHECKPOINT_EVERY == 0
                or position == total
            ):
                save_checkpoint(processed_ids)

            if (
                position % PROGRESS_EVERY == 0
                or position == total
            ):
                elapsed = monotonic() - started
                average = elapsed / position
                remaining_count = total - position
                estimated_remaining = average * remaining_count
                percent = position / total * 100

                print(
                    f"Processed {position:,}/{total:,} "
                    f"({percent:.1f}%) | "
                    f"Current: {business_name} — {town}"
                )
                print(
                    f"Accepted: {accepted:,} | "
                    f"Rejected: {rejected:,} | "
                    f"Errors: {errors:,} | "
                    f"Elapsed: {format_duration(elapsed)} | "
                    f"ETA: {format_duration(estimated_remaining)}"
                )

    except KeyboardInterrupt:
        save_checkpoint(processed_ids)
        print()
        print("Crawl stopped safely. Progress was checkpointed.")
        print("Run the same command later to resume.")
        return

    output_path = save_report_workbook(
        df=df,
        source_path=workbook,
        suffix="free_website_crawl_preview",
    )

    print()
    print("=" * 70)
    print("Free Website Crawl Complete")
    print("=" * 70)
    print(f"Businesses processed: {total:,}")
    print(f"Updates accepted: {accepted:,}")
    print(f"Updates rejected: {rejected:,}")
    print(f"Updates applied to preview: {applied:,}")
    print(f"Errors skipped: {errors:,}")
    print(f"Saved preview workbook to: {output_path}")


if __name__ == "__main__":
    run()
