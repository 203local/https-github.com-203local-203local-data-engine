import pandas as pd

from app.core.workbook import find_master_workbook


IMPORTANT_FIELDS = [
    "website",
    "email",
    "phone",
    "facebook",
    "instagram",
    "google_maps_url",
    "google_rating",
    "google_review_count",
    "seo_directory_title",
    "seo_meta_description",
    "restaurant_intelligence_notes",
]


def run():
    workbook = find_master_workbook()

    if workbook is None:
        print("No master workbook found.")
        return

    df = pd.read_excel(workbook)

    business = input("Business name: ").strip().lower()

    matches = df[
        df["post_title"]
        .fillna("")
        .str.lower()
        .str.contains(business, regex=False, na=False)
    ]

    if matches.empty:
        print("No match found.")
        return

    row = matches.iloc[0]

    print()
    print("=" * 50)
    print(row["post_title"])
    print("=" * 50)

    score = 0

    for field in IMPORTANT_FIELDS:
        value = str(row.get(field, "")).strip()
        complete = value not in ("", "nan")

        if complete:
            score += 1

        print(f"{field:35} {'✅' if complete else '❌'}")

    percent = round(score / len(IMPORTANT_FIELDS) * 100)

    print()
    print(f"Overall completeness: {percent}%")
