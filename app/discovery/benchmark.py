import pandas as pd

from app.discovery.website_discovery import discover_official_website


def run(limit=100):
    df = pd.read_excel("master/203local_Master_Directory.xlsx")

    missing = df[
        df["website"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
    ].head(limit)

    stats = {
        "processed": 0,
        "found": 0,
        "high_confidence": 0,
        "manual_review": 0,
    }

    print("=" * 80)
    print("Website Discovery Benchmark")
    print("=" * 80)

    for _, row in missing.iterrows():
        name = row.get("post_title", "")
        town = row.get("town", "")

        result = discover_official_website(name, town)

        stats["processed"] += 1

        if result.website:
            stats["found"] += 1

        if result.confidence >= 0.90:
            stats["high_confidence"] += 1
        else:
            stats["manual_review"] += 1

        print(f"{name} ({town})")
        print(f"  Website: {result.website or 'None'}")
        print(f"  Confidence: {result.confidence:.2f}")
        print(f"  Reason: {result.reason}")
        print()

    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Processed:        {stats['processed']}")
    print(f"Websites found:   {stats['found']}")
    print(f"High confidence:  {stats['high_confidence']}")
    print(f"Manual review:    {stats['manual_review']}")
