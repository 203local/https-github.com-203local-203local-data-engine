import time
import pandas as pd

from app.discovery.website_discovery import discover_official_website


def run(limit=25):
    df = pd.read_excel("master/203local_Master_Directory.xlsx")

    missing = df[
        df["website"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
    ].head(limit)

    total = len(missing)

    print("=" * 70)
    print("Website Discovery Job")
    print("=" * 70)

    for i, (_, row) in enumerate(missing.iterrows(), start=1):
        print(f"[{i}/{total}] {row['post_title']} ({row['town']})")

        result = discover_official_website(
            row["post_title"],
            row["town"],
        )

        print(f"  Website: {result.website or 'None'}")
        print(f"  Confidence: {result.confidence:.2f}")

        # Small pause to avoid hammering APIs
        time.sleep(0.25)

    print()
    print("Job complete.")
