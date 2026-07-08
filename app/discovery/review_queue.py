import pandas as pd

from app.discovery.website_discovery import discover_official_website


def build_review_queue(limit=100):
    df = pd.read_excel("master/203local_Master_Directory.xlsx")

    missing = df[
        df["website"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
    ].head(limit)

    rows = []

    for _, row in missing.iterrows():
        result = discover_official_website(
            row["post_title"],
            row["town"],
        )

        if result.confidence >= 0.90:
            continue

        rows.append({
            "business_id": row["business_id"],
            "business_name": row["post_title"],
            "town": row["town"],
            "suggested_website": result.website,
            "confidence": result.confidence,
            "reason": result.reason,
            "approved_website": "",
        })

    review = pd.DataFrame(rows)

    review.to_excel(
        "reports/website_review_queue.xlsx",
        index=False,
    )

    print()
    print("=" * 70)
    print("Review Queue Created")
    print("=" * 70)
    print("Businesses requiring review:", len(review))
    print("Saved to reports/website_review_queue.xlsx")
