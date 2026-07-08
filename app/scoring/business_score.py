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


def calculate_health_score(row):
    score = 0

    for field, weight in WEIGHTS.items():
        value = str(row.get(field, "")).strip()

        if value and value.lower() != "nan":
            score += weight

    return score
