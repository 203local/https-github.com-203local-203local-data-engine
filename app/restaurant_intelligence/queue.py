from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from config import MASTER_FILE
from app.restaurant_intelligence.config import QUEUE_FILE, BATCH_FOLDER, TARGET_FIELDS


def is_blank(value):
    return pd.isna(value) or str(value).strip().lower() in {"", "nan"}


def looks_like_food_business(row):
    fields = [
        "primary_category",
        "primary_business_type",
        "business_types",
        "website_directory_category",
    ]

    text = " ".join(str(row.get(field, "")) for field in fields).lower()

    keywords = [
        "restaurant",
        "food",
        "cafe",
        "coffee",
        "bakery",
        "bar",
        "brewery",
        "pizza",
        "deli",
        "market",
        "catering",
        "ice cream",
        "juice",
    ]

    return any(keyword in text for keyword in keywords)


def needs_restaurant_intelligence(row):
    important_fields = [
        "cuisine_primary",
        "cuisines",
        "service_tags",
        "amenities_tags",
        "dietary_tags",
        "restaurant_intelligence_notes",
    ]

    return any(is_blank(row.get(field, "")) for field in important_fields)


def generate_restaurant_intelligence_queue():
    BATCH_FOLDER.mkdir(parents=True, exist_ok=True)

    master = pd.read_excel(MASTER_FILE, dtype=str)

    eligible = master[
        master.apply(looks_like_food_business, axis=1)
        & master["website"].apply(lambda x: not is_blank(x))
        & master.apply(needs_restaurant_intelligence, axis=1)
    ].copy()

    base_columns = [
        "business_id",
        "post_title",
        "town",
        "county",
        "website",
        "primary_category",
        "primary_business_type",
        "business_types",
        "website_directory_category",
    ]

    queue = eligible[base_columns + TARGET_FIELDS].copy()

    suggested_fields = [
        "suggested_cuisine_primary",
        "suggested_cuisines",
        "suggested_offerings_tags",
        "suggested_service_tags",
        "suggested_amenities_tags",
        "suggested_dietary_tags",
        "suggested_service_model_tags",
        "suggested_price_range",
        "suggested_has_menu_link",
        "suggested_serves_alcohol_signal",
        "suggested_has_reservations",
        "suggested_offers_online_ordering",
        "suggested_offers_delivery",
        "suggested_offers_takeout",
        "suggested_offers_catering",
        "suggested_private_events_available",
        "suggested_has_happy_hour",
        "suggested_has_brunch",
        "suggested_has_breakfast",
        "suggested_outdoor_dining_signal",
        "suggested_live_music_signal",
        "suggested_dog_friendly_signal",
        "suggested_kid_friendly_signal",
        "suggested_dietary_options_signal",
        "suggested_restaurant_intelligence_notes",
    ]

    for field in suggested_fields:
        queue[field] = ""

    queue["source_url"] = ""
    queue["confidence"] = ""
    queue["review_status"] = "Needs Review"
    queue["ready_to_merge"] = "No"
    queue["notes"] = ""

    queue.to_csv(QUEUE_FILE, index=False)

    print("=" * 70)
    print("Restaurant Intelligence Queue Created")
    print("=" * 70)
    print("Master file:", MASTER_FILE)
    print("Eligible businesses:", len(queue))
    print("Queue file:", QUEUE_FILE)


if __name__ == "__main__":
    generate_restaurant_intelligence_queue()
