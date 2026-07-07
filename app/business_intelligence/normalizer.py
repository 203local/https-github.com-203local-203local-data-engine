import json


def yes_no(value):
    if value is True:
        return "Yes"
    if value is False:
        return "No"
    return ""


def normalize_list(value):
    if value is None:
        return "[]"
    if isinstance(value, list):
        return json.dumps(sorted(set(value)))
    return str(value)


def normalize_confidence(value):
    try:
        v = float(value)
        if v <= 1:
            v *= 100
        return str(round(v))
    except Exception:
        return ""


def normalize_business_result(result):
    result["business_types"] = normalize_list(result.get("business_types"))
    result["offerings_tags"] = normalize_list(result.get("offerings_tags"))
    result["service_tags"] = normalize_list(result.get("service_tags"))
    result["amenities_tags"] = normalize_list(result.get("amenities_tags"))
    result["audience_tags"] = normalize_list(result.get("audience_tags"))
    result["ownership_tags"] = normalize_list(result.get("ownership_tags"))
    result["service_model_tags"] = normalize_list(result.get("service_model_tags"))
    result["searchable_keywords"] = normalize_list(result.get("searchable_keywords"))

    result["review_needed"] = yes_no(result.get("review_needed"))
    result["existing_data_conflict"] = yes_no(result.get("existing_data_conflict"))

    result["confidence"] = normalize_confidence(result.get("confidence"))

    return result


if __name__ == "__main__":
    sample = {
        "business_types": ["Restaurant", "Pizza"],
        "offerings_tags": ["Delivery", "Takeout"],
        "review_needed": True,
        "existing_data_conflict": False,
        "confidence": 0.94,
    }

    print(normalize_business_result(sample))
