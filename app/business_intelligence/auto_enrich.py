import pandas as pd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.ai.business_client import generate_business_intelligence
from app.business_intelligence.config import BATCH_FOLDER, RESULTS_FOLDER


def run(limit=5):
    RESULTS_FOLDER.mkdir(parents=True, exist_ok=True)

    batch_files = sorted(BATCH_FOLDER.glob("business_intelligence_batch_*.csv"))

    if not batch_files:
        print("No business intelligence batches found.")
        return

    batch_file = batch_files[0]

    df = pd.read_csv(batch_file, dtype=str)

    if limit:
        df = df.head(limit).copy()

    print("=" * 70)
    print("Business Intelligence Auto Enrichment")
    print("=" * 70)
    print("Batch:", batch_file.name)
    print("Limit:", len(df))

    output_rows = []

    for _, row in df.iterrows():
        print("Enriching:", row["post_title"])

        result = generate_business_intelligence(row.to_dict())

        output = row.to_dict()

        for key, value in result.items():
            output[f"suggested_{key}"] = value

        output["review_status"] = "Business Intelligence Suggested"
        output["ready_to_merge"] = "No"
        output["confidence"] = result.get("confidence", "")
        output["notes"] = result.get("reason", "")

        output_rows.append(output)

        print("  ✓ Suggested")

    output_file = RESULTS_FOLDER / batch_file.name.replace(".csv", "_results.csv")

    pd.DataFrame(output_rows).to_csv(output_file, index=False)

    print("=" * 70)
    print("Business intelligence auto enrichment complete")
    print("Processed:", len(output_rows))
    print("Results:", output_file)


if __name__ == "__main__":
    run()
