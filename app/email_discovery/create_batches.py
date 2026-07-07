from pathlib import Path
import sys
import math
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.email_discovery.queue import QUEUE_FILE
from app.email_discovery.config import BATCH_FOLDER


BATCH_SIZE = 100


def create_email_batches():
    if not QUEUE_FILE.exists():
        print("Queue file not found. Run:")
        print("python3 -m app.email_discovery.queue")
        return

    queue = pd.read_csv(QUEUE_FILE)
    total = len(queue)
    batches = math.ceil(total / BATCH_SIZE)

    print("=" * 70)
    print("Creating Email Discovery Batches")
    print("=" * 70)

    for i in range(batches):
        start = i * BATCH_SIZE
        end = start + BATCH_SIZE
        batch = queue.iloc[start:end].copy()

        batch_file = BATCH_FOLDER / f"email_batch_{i + 1:04d}.csv"
        batch.to_csv(batch_file, index=False)

        print(f"Created {batch_file.name}: {len(batch)} rows")

    print("=" * 70)
    print(f"Total batches created: {batches}")


if __name__ == "__main__":
    create_email_batches()
