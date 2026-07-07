BUSINESS_INTELLIGENCE_PROMPT = """
You are extracting structured business intelligence for the 203local business directory.

Use ONLY the supplied directory record and website content.
Do not guess.
If a field cannot be determined, return null.
Return ONLY valid JSON.

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
