import json


SERVICE_MAP = {
    "take-out": "Takeout",
    "takeout": "Takeout",
    "carryout": "Takeout",
    "carry-out": "Takeout",
    "pickup": "Takeout",
    "pick-up": "Takeout",
    "dine-in": "Dine-in",
    "dine in": "Dine-in",
    "delivery": "Delivery",
    "catering": "Catering",
}

CUISINE_MAP = {
    "mexican / latin": "Mexican",
    "burgers / sandwiches": "American",
    "chinese / soup dumplings": "Chinese",
}


def parse_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return value

    text = str(value).strip()

    if not text or text.lower() in {"nan", "null", "none"}:
        return []

    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return parsed
    except Exception:
        pass

    return [item.strip() for item in text.split(",") if item.strip()]


def normalize_list(value, mapping=None):
    mapping = mapping or {}
    items = parse_list(value)
    cleaned = []

    for item in items:
        key = str(item).strip().lower()
        normalized = mapping.get(key, str(item).strip())

        if normalized and normalized not in cleaned:
            cleaned.append(normalized)

    return json.dumps(sorted(cleaned))


def normalize_confidence(value):
    if value is None:
        return ""

    text = str(value).strip().lower()

    if not text or text in {"nan", "null", "none"}:
        return ""

    if text in {"high"}:
        return "90"
    if text in {"medium"}:
        return "70"
    if text in {"low"}:
        return "50"

    try:
        number = float(text)
    except Exception:
        return ""

    if number <= 1:
        number = number * 100
    elif number <= 10:
        number = number * 10

    return str(int(round(number)))


def normalize_bool(value):
    if value is None:
        return ""

    text = str(value).strip().lower()

    if text in {"true", "yes", "y", "1"}:
        return "Yes"

    if text in {"false", "no", "n", "0"}:
        return "No"

    return ""


def normalize_text(value):
    if value is None:
        return ""

    text = str(value).strip()

    if text.lower() in {"nan", "null", "none"}:
        return ""

    return text


def normalize_cuisine_primary(value):
    text = normalize_text(value)
    key = text.lower()
    return CUISINE_MAP.get(key, text)


def normalize_restaurant_result(result):
    normalized = dict(result)

    normalized["cuisine_primary"] = normalize_cuisine_primary(
        result.get("cuisine_primary")
    )

    normalized["cuisines"] = normalize_list(
        result.get("cuisines"),
        CUISINE_MAP,
    )

    normalized["service_model_tags"] = normalize_list(
        result.get("service_model_tags"),
        SERVICE_MAP,
    )

    for field in [
        "offerings_tags",
        "service_tags",
        "amenities_tags",
        "dietary_tags",
    ]:
        normalized[field] = normalize_list(result.get(field))

    for field in [
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
    ]:
        normalized[field] = normalize_bool(result.get(field))

    normalized["confidence"] = normalize_confidence(result.get("confidence"))
    normalized["restaurant_intelligence_notes"] = normalize_text(
        result.get("restaurant_intelligence_notes")
    )

    return normalized


if __name__ == "__main__":
    sample = {
        "cuisine_primary": "Mexican / Latin",
        "cuisines": ["Mexican / Latin", "Pizza"],
        "service_model_tags": ["Take-Out", "Pickup", "Delivery"],
        "offers_catering": True,
        "has_menu_link": "true",
        "confidence": 0.9,
    }

    print(normalize_restaurant_result(sample))
