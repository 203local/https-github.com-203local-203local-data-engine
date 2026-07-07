import json
import os

from openai import OpenAI

from app.ai.prompts import AI_ENRICHMENT_PROMPT
from app.ai.models import business_record_to_text
from app.ai.webpage import extract_text


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ai_enrichment(record):
    business_text = business_record_to_text(record)

    website = record.get("website", "")
    website_text = extract_text(website, max_chars=7000)

    combined_input = f"""
DIRECTORY RECORD
----------------
{business_text}

WEBSITE CONTENT
---------------
{website_text}
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": AI_ENRICHMENT_PROMPT,
                },
                {
                    "role": "user",
                    "content": combined_input,
                },
            ],
            text={
                "format": {
                    "type": "json_object"
                }
            },
        )

        content = response.output_text
        result = json.loads(content)

    except Exception as e:
        result = {
            "post_content": "",
            "seo_directory_title": "",
            "seo_meta_description": "",
            "searchable_keywords": "",
            "confidence": "Failed",
            "reason": f"AI API error: {e}",
        }

    result["business_input"] = combined_input
    result["prompt_used"] = AI_ENRICHMENT_PROMPT.strip()

    return result


if __name__ == "__main__":
    sample = {
        "post_title": "Los Alebrijes",
        "town": "Bridgeport",
        "primary_category": "Restaurant",
        "website": "https://losalebrijesct.com",
    }

    print(json.dumps(generate_ai_enrichment(sample), indent=2))
