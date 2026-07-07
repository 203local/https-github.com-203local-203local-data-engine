import json

from app.ai.engine import generate_structured_json
from app.ai.models import business_record_to_text
from app.ai.restaurant_prompt import RESTAURANT_INTELLIGENCE_PROMPT
from app.ai.webpage import extract_text


def generate_restaurant_intelligence(record):
    business_text = business_record_to_text(record)

    website = record.get("website", "")
    website_text = extract_text(website, max_chars=8000)

    combined_input = f"""
DIRECTORY RECORD
----------------
{business_text}

WEBSITE CONTENT
---------------
{website_text}
"""

    result = generate_structured_json(
        RESTAURANT_INTELLIGENCE_PROMPT,
        combined_input,
    )

    result["business_input"] = combined_input
    result["source_url"] = website
    return result


if __name__ == "__main__":
    sample = {
        "post_title": "Los Alebrijes",
        "town": "Bridgeport",
        "county": "Fairfield",
        "primary_category": "Restaurant",
        "website": "https://losalebrijesct.com",
    }

    print(json.dumps(generate_restaurant_intelligence(sample), indent=2))
