from app.completeness.checker import CompletenessResult

IMPORTANT_FIELDS = {
    "website": "Website Repair",
    "email": "Email Discovery",
    "google_maps_url": "Google Business Repair",
    "google_rating": "Google Business Repair",
    "google_review_count": "Google Business Repair",
    "seo_directory_title": "SEO Repair",
    "seo_meta_description": "SEO Repair",
    "restaurant_intelligence_notes": "Restaurant Intelligence",
}


def analyze(row):
    missing = []
    repairs = set()

    for field, repair in IMPORTANT_FIELDS.items():
        value = str(row.get(field, "")).strip()

        if value in ("", "nan", "None"):
            missing.append(field)
            repairs.add(repair)

    score = round(
        ((len(IMPORTANT_FIELDS) - len(missing)) / len(IMPORTANT_FIELDS)) * 100
    )

    return CompletenessResult(
        score=score,
        missing_fields=missing,
        suggested_repairs=sorted(repairs),
    )
