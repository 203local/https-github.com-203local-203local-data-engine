import json

from app.ai.engine import generate_structured_json
from app.ai.webpage import extract_text
from app.ai.business_prompt import BUSINESS_INTELLIGENCE_PROMPT
from app.ai.models import business_record_to_text


def generate_business_intelligence(record):
    website = record.get("website", "")
    website_text = extract_text(website)

    business_text = business_record_to_text(record)

    combined_input = f"""
DIRECTORY RECORD
----------------
{business_text}

WEBSITE CONTENT
---------------
{website_text}
"""

    result = generate_structured_json(
        BUSINESS_INTELLIGENCE_PROMPT,
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
        "website": "https://losalebrijesct.com",
        "primary_category": "Restaurant",
    }

    print(json.dumps(generate_business_intelligence(sample), indent=2))
