import pandas as pd

from app.core.workbook import find_master_workbook
from app.jobs.website_discovery.search import build_google_search_url


def run(limit=100):
    workbook = find_master_workbook()

    if workbook is None:
        print("No master workbook found.")
        return

    df = pd.read_excel(workbook)

    missing_google = df[
        df["google_maps_url"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
    ].copy()

    missing_google["google_search_url"] = missing_google.apply(
        lambda row: build_google_search_url(
            row.get("post_title", ""),
            row.get("town", ""),
        ),
        axis=1,
    )

    output = missing_google[
        [
            "post_title",
            "town",
            "phone",
            "website",
            "google_search_url",
        ]
    ].head(limit)

    print()
    print("=" * 75)
    print("Google Business Candidate Report")
    print("=" * 75)
    print(output.to_string(index=False))
