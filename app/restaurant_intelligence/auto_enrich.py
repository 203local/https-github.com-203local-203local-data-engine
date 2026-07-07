from pathlib import Path
import sys
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.ai.restaurant_client import generate_restaurant_intelligence
from app.restaurant_intelligence.normalizer import normalize_restaurant_result
from app.restaurant_intelligence.config import RESULTS_FOLDER
from app.restaurant_intelligence.config import BATCH_FOLDER


def find_current_batch():
    batches = sorted(BATCH_FOLDER.glob("restaurant_intelligence_batch_*.csv"))
    if not batches:
        return None

    for batch in batches:
        result_file = RESULTS_FOLDER / batch.name.replace(".csv", "_results.csv")
        if not result_file.exists():
            return batch

    return batches[0]


def as_text(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value)
    if value is None:
        return ""
    return str(value)


def run(limit=5):
    RESULTS_FOLDER.mkdir(parents=True, exist_ok=True)

    batch_file = find_current_batch()

    if batch_file is None:
        print("No restaurant intelligence batches found.")
        return

    output_file = RESULTS_FOLDER / batch_file.name.replace(".csv", "_results.csv")

    if output_file.exists():
        df = pd.read_csv(output_file, dtype=str)
    else:
        df = pd.read_csv(batch_file, dtype=str)

    processed = 0

    print("=" * 70)
    print("Restaurant Intelligence Auto Enrichment")
    print("=" * 70)
    print("Batch:", batch_file.name)
    print("Limit:", limit)

    for idx, row in df.iterrows():
        if processed >= limit:
            break

        status = str(row.get("review_status", "")).strip().lower()
        if status and status != "needs review":
            continue

        print("Enriching:", row.get("post_title", ""))

        result = generate_restaurant_intelligence(row.to_dict())
        result = normalize_restaurant_result(result)

        for key, value in result.items():
            if key in {"business_input", "reason", "source_url"}:
                continue

            suggested_col = f"suggested_{key}"
            if suggested_col in df.columns:
                df.at[idx, suggested_col] = as_text(value)

        df.at[idx, "source_url"] = result.get("source_url", row.get("website", ""))
        df.at[idx, "confidence"] = as_text(result.get("confidence", ""))
        df.at[idx, "notes"] = result.get("reason", "")
        df.at[idx, "review_status"] = "Restaurant Intelligence Suggested"
        df.at[idx, "ready_to_merge"] = "No"

        df.to_csv(output_file, index=False)

        processed += 1
        print("  ✓ Suggested")

    print("=" * 70)
    print("Restaurant intelligence auto enrichment complete")
    print("Processed:", processed)
    print("Results:", output_file)


if __name__ == "__main__":
    run()
