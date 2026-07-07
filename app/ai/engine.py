import json
import os

from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_structured_json(system_prompt, user_input, model="gpt-4.1-mini"):
    """
    Shared AI engine for all structured enrichment jobs.

    Used by:
    - AI Enrichment
    - Restaurant Intelligence
    - Future Social Discovery
    - Future Event Intelligence
    """

    try:
        response = client.responses.create(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
            text={
                "format": {
                    "type": "json_object"
                }
            },
        )

        return json.loads(response.output_text)

    except Exception as e:
        return {
            "confidence": "Failed",
            "reason": f"AI API error: {e}",
        }
