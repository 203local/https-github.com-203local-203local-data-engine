from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from app.ai.client import generate_ai_enrichment
from app.ai_enrichment.batch_manager import find_current_batch
from app.ai_enrichment.config import RESULTS_FOLDER


def run(limit=5):
    RESULTS_FOLDER.mkdir(parents=True, exist_ok=True)

    batch_file = find_current_batch()

    if batch_file is None:
        print("No AI enrichment batches found.")
        return

    output_file = RESULTS_FOLDER / batch_file.name.replace(".csv", "_results.csv")

    if output_file.exists():
        df = pd.read_csv(output_file, dtype=str)
    else:
        df = pd.read_csv(batch_file, dtype=str)

    processed = 0

    print("=" * 70)
    print("AI Auto Enrichment")
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

        result = generate_ai_enrichment(row.to_dict())

        df.at[idx, "suggested_post_content"] = result.get("post_content", "")
        df.at[idx, "suggested_seo_directory_title"] = result.get("seo_directory_title", "")
        df.at[idx, "suggested_seo_meta_description"] = result.get("seo_meta_description", "")
        df.at[idx, "suggested_searchable_keywords"] = result.get("searchable_keywords", "")
        df.at[idx, "confidence"] = result.get("confidence", "")
        df.at[idx, "notes"] = result.get("reason", "")
        df.at[idx, "source_url"] = row.get("website", "")
        df.at[idx, "review_status"] = "AI Suggested"
        df.at[idx, "ready_to_merge"] = "No"

        df.to_csv(output_file, index=False)

        processed += 1
        print("  ✓ Suggested")

    print("=" * 70)
    print("AI auto enrichment complete")
    print("Processed:", processed)
    print("Results:", output_file)


if __name__ == "__main__":
    run()
