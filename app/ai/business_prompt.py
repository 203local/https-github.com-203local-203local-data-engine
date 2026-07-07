BUSINESS_INTELLIGENCE_PROMPT = """
You are extracting structured business intelligence and quality assurance signals for the 203local business directory.

Use ONLY the supplied directory record and website content.
Do not guess.
If a field cannot be determined, return null.
Return ONLY valid JSON.

Important rules:
- Preserve existing primary_category and primary_business_type unless the website clearly proves they are wrong.
- Do not silently overwrite primary_category or primary_business_type.
- If the existing category/type appears wrong, return the better suggestion AND set review_needed to true.
- If the existing data conflicts with the website, set existing_data_conflict to true.
- Do not invent amenities, ownership, audience, or services.
- If website content is unavailable, rely on the directory record only and use low confidence.

Return this JSON structure:

{
  "primary_category": null,
  "primary_business_type": null,
  "business_types": [],
  "offerings_tags": [],
  "service_tags": [],
  "amenities_tags": [],
  "audience_tags": [],
  "ownership_tags": [],
  "service_model_tags": [],
  "searchable_keywords": [],
  "business_intelligence_notes": "",
  "review_needed": false,
  "review_reason": "",
  "existing_data_conflict": false,
  "confidence": 0,
  "reason": ""
}
"""
