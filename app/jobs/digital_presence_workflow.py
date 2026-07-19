from pathlib import Path

import pandas as pd

from app.jobs.website_review_manager import review_batch
from app.merge.safe_merge_manager import merge_research_batch


BATCH_DIRECTORY = Path(
    "enrichment/missing_website_batches"
)

PENDING_STATUSES = {
    "",
    "pending",
    "needs review",
}


def clean(value):
    if value is None:
        return ""

    value = str(value).strip()

    if value.casefold() == "nan":
        return ""

    return value


def load_batch(batch_path):
    return pd.read_csv(
        batch_path,
        dtype=str,
    ).fillna("")


def count_pending(df):
    if "research_status" not in df.columns:
        return len(df)

    statuses = (
        df["research_status"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.casefold()
    )

    return int(statuses.isin(PENDING_STATUSES).sum())


def find_batches():
    if not BATCH_DIRECTORY.exists():
        raise FileNotFoundError(
            f"Batch directory not found: {BATCH_DIRECTORY}"
        )

    return [
        path
        for path in sorted(
            BATCH_DIRECTORY.glob("*.csv")
        )
        if "_test" not in path.stem.casefold()
    ]


def show_dashboard(batches):
    print()
    print("=" * 72)
    print("203local Digital Presence Workflow")
    print("=" * 72)
    print()

    total_rows = 0
    total_pending = 0
    batch_details = []

    for batch_path in batches:
        try:
            df = load_batch(batch_path)
            pending = count_pending(df)
            total = len(df)
        except Exception as exc:
            batch_details.append(
                (
                    batch_path,
                    0,
                    0,
                    f"ERROR: {exc}",
                )
            )
            continue

        total_rows += total
        total_pending += pending

        if pending == 0:
            status = "COMPLETE"
        elif pending == total:
            status = "NOT STARTED"
        else:
            status = "IN PROGRESS"

        batch_details.append(
            (
                batch_path,
                total,
                pending,
                status,
            )
        )

    for batch_path, total, pending, status in batch_details:
        reviewed = total - pending

        print(
            f"{batch_path.name:<42} "
            f"{status:<12} "
            f"{reviewed:>3}/{total:<3} reviewed"
        )

    reviewed_total = total_rows - total_pending

    print()
    print("-" * 72)
    print(f"Total businesses:   {total_rows}")
    print(f"Reviewed:           {reviewed_total}")
    print(f"Still pending:      {total_pending}")

    if total_rows:
        percent = reviewed_total / total_rows * 100
        print(f"Progress:           {percent:.1f}%")

    print()

    return batch_details


def find_next_batch(batch_details):
    for batch_path, total, pending, status in batch_details:
        if status.startswith("ERROR"):
            continue

        if pending > 0:
            return batch_path

    return None


def run():
    batches = find_batches()

    if not batches:
        print(
            f"No research batches found in "
            f"{BATCH_DIRECTORY}."
        )
        return

    batch_details = show_dashboard(batches)
    next_batch = find_next_batch(batch_details)

    if next_batch is None:
        print("All available batches are reviewed.")
        return

    print(f"Next batch: {next_batch}")
    print()

    choice = input(
        "Open this batch for review? [Y/n]: "
    ).strip().casefold()

    if choice not in {"", "y", "yes"}:
        print("Review not started.")
        return

    review_batch(next_batch)

    refreshed = load_batch(next_batch)
    pending = count_pending(refreshed)

    if pending:
        print()
        print(
            f"{pending} businesses remain pending "
            f"in {next_batch.name}."
        )
        return

    print()
    print("Batch review is complete.")

    dry_run_choice = input(
        "Run the Safe Merge Manager dry run? [Y/n]: "
    ).strip().casefold()

    if dry_run_choice not in {"", "y", "yes"}:
        print("Dry run not started.")
        return

    merge_research_batch(
        str(next_batch),
        dry_run=True,
    )


if __name__ == "__main__":
    run()
