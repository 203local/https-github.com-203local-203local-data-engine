import pandas as pd


def generate_summary(report_file):
    df = pd.read_csv(report_file)

    df = df.sort_values(
        by=["quality_score", "issue_count", "post_title"],
        ascending=[True, False, True],
    )

    print("=" * 70)
    print("Lowest Quality Businesses")
    print("=" * 70)

    cols = [
        "post_title",
        "town",
        "quality_score",
        "quality_band",
        "issue_count",
        "issues",
    ]

    print(df.head(25)[cols].to_string(index=False))

    return df
