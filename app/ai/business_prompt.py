BUSINESS_INTELLIGENCE_PROMPT = """
You are extracting structured business intelligence for the 203local business directory.

Use ONLY the supplied directory record and website content.
Do not guess.
If a field cannot be determined, return null.
Return ONLY valid JSON.

Important rules:
- Preserve the existing primary_category and primary_business_type unless the website clearly proves they are wrong.
- Do not downgrade or generalize a known business type.
- If the directory says Pizza, Restaurant, Deli, Bakery, Bar, Salon, etc., keep that context.
- Business types should be specific and practical for directory filtering.
- Do not classify pizza restaurants as coffee shops.
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
  "confidence": 0,
  "reason": ""
}
"""
