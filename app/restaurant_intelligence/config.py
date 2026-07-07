from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

BATCH_FOLDER = ROOT / "enrichment" / "restaurant_intelligence_batches"
RESULTS_FOLDER = ROOT / "enrichment" / "restaurant_intelligence_results"
LOG_FOLDER = ROOT / "enrichment" / "restaurant_intelligence_logs"

QUEUE_FILE = BATCH_FOLDER / "restaurant_intelligence_queue.csv"

BATCH_SIZE = 50

TARGET_FIELDS = [
    "cuisine_primary",
    "cuisines",
    "offerings_tags",
    "service_tags",
    "amenities_tags",
    "dietary_tags",
    "service_model_tags",
    "price_range",
    "has_menu_link",
    "serves_alcohol_signal",
    "has_reservations",
    "offers_online_ordering",
    "offers_delivery",
    "offers_takeout",
    "offers_catering",
    "private_events_available",
    "has_happy_hour",
    "has_brunch",
    "has_breakfast",
    "outdoor_dining_signal",
    "live_music_signal",
    "dog_friendly_signal",
    "kid_friendly_signal",
    "dietary_options_signal",
    "restaurant_intelligence_confidence",
    "restaurant_intelligence_review_needed",
    "restaurant_intelligence_notes",
    "restaurant_intelligence_source",
    "restaurant_intelligence_updated_date",
]
