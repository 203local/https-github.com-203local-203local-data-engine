from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT))

BATCH_FILE = ROOT / "enrichment" / "batches" / "website_batch_0001.csv"
OUTPUT_FILE = ROOT / "enrichment" / "results" / "website_batch_0001_discovery_results.csv"

def run():
    print("Website Discovery Job v1")
    print("Reading batch:", BATCH_FILE)

    df = pd.read_csv(BATCH_FILE)

    df["discovery_status"] = "Queued"
    df["suggested_website"] = df.get("suggested_website", "")
    df["confidence"] = df.get("confidence", "")
    df["notes"] = "Ready for website discovery"

    df.to_csv(OUTPUT_FILE, index=False)

    print("Rows queued:", len(df))
    print("Output:", OUTPUT_FILE)

if __name__ == "__main__":
    run()
