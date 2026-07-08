import pandas as pd

from app.core.workbook import find_master_workbook


WEIGHTS = {
    "website": 15,
    "email": 15,
    "phone": 10,
    "facebook": 5,
    "instagram": 5,
    "google_maps_url": 10,
    "google_rating": 10,
    "google_review_count": 5,
    "seo_directory_title": 10,
    "seo_meta_description": 10,
    "restaurant_intelligence_notes": 5,
}


def score_row(row):
    score = 0

    for field, weight in WEIGHTS.items():
        value = str(row.get(field, "")).strip()

        if value and value.lower() != "nan":
            score += weight

    return score


def run():
    workbook = find_master_workbook()

    if workbook is None:
        print("No master workbook found.")
        return

    df = pd.read_excel(workbook)

    df["health_score"] = df.apply(score_row, axis=1)

    print()
    print("=" * 70)
    print("203local Business Health Dashboard")
    print("=" * 70)
    print()

    print(
        df[
            ["post_title", "town", "health_score"]
        ]
        .sort_values("health_score")
        .head(25)
        .to_string(index=False)
    )

    print()
    print(f"Average Health Score: {df['health_score'].mean():.1f}/100")
