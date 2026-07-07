from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

QUEUE_FOLDER = ROOT / "enrichment" / "queues"
BATCH_FOLDER = ROOT / "enrichment" / "batches"

BATCH_SIZE = 100

def latest_queue_file():
    files = sorted(QUEUE_FOLDER.glob("missing_websites_queue_*.csv"))
    if not files:
        print("No missing website queue files found.")
        raise SystemExit(1)
    return files[-1]

def create_batches():
    print("Creating website discovery batches...")

    BATCH_FOLDER.mkdir(parents=True, exist_ok=True)

    queue_file = latest_queue_file()
    df = pd.read_csv(queue_file)

    total = len(df)
    batch_count = 0

    for start in range(0, total, BATCH_SIZE):
        batch_count += 1
        batch = df.iloc[start:start + BATCH_SIZE].copy()
        out_path = BATCH_FOLDER / f"website_batch_{batch_count:04d}.csv"
        batch.to_csv(out_path, index=False)

    print("Source queue:", queue_file)
    print(f"Total businesses: {total:,}")
    print(f"Batches created: {batch_count:,}")
    print("Batch folder:", BATCH_FOLDER)

if __name__ == "__main__":
    create_batches()
