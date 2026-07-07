import math
from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.ai_enrichment.config import QUEUE_FILE, BATCH_FOLDER, BATCH_SIZE


def create_ai_batches():
    if not QUEUE_FILE.exists():
        print("Queue file not found. Run:")
        print("python3 -m app.ai_enrichment.queue")
        return

    queue = pd.read_csv(QUEUE_FILE, dtype=str)
    total = len(queue)
    batches = math.ceil(total / BATCH_SIZE)

    print("=" * 70)
    print("Creating AI Enrichment Batches")
    print("=" * 70)

    for i in range(batches):
        start = i * BATCH_SIZE
        end = start + BATCH_SIZE
        batch = queue.iloc[start:end].copy()

        batch_file = BATCH_FOLDER / f"ai_batch_{i + 1:04d}.csv"
        batch.to_csv(batch_file, index=False)

        print(f"Created {batch_file.name}: {len(batch)} rows")

    print("=" * 70)
    print(f"Total batches created: {batches}")


if __name__ == "__main__":
    create_ai_batches()
