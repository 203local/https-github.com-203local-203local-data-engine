import json
from app.ai.prompts import AI_ENRICHMENT_PROMPT
from app.ai.models import business_record_to_text


def generate_ai_enrichment(record):
    """
    Placeholder AI client.

    This returns structured draft data without calling an external AI API yet.
    Later, this function will call OpenAI or another provider.
    """
    business_text = business_record_to_text(record)

    name = record.get("post_title", "")
    town = record.get("town", "")
    category = record.get("primary_category", "") or record.get("primary_business_type", "")

    post_content = f"{name} is a local business in {town}."
    if category and str(category).strip().lower() != "nan":
        post_content += f" It is listed under {category}."

    result = {
        "post_content": post_content,
        "seo_directory_title": f"{name} | {town} CT | 203local",
        "seo_meta_description": f"Find information about {name} in {town}, CT on 203local.",
        "searchable_keywords": f"{name}, {town}, CT, {category}",
        "confidence": "Low",
        "reason": "Placeholder AI enrichment generated from existing directory fields only.",
        "prompt_used": AI_ENRICHMENT_PROMPT.strip(),
        "business_input": business_text,
    }

    return result


if __name__ == "__main__":
    sample = {
        "post_title": "Sample Restaurant",
        "town": "Fairfield",
        "primary_category": "Restaurant",
    }

    print(json.dumps(generate_ai_enrichment(sample), indent=2))
