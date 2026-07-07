RESTAURANT_INTELLIGENCE_PROMPT = """
You are extracting structured restaurant intelligence for the 203local business directory.

Use ONLY the supplied directory record and website content.
Do not guess.
If a field cannot be determined, return null.
Return ONLY valid JSON.

Return this JSON structure:

{
  "cuisine_primary": null,
  "cuisines": [],
  "offerings_tags": [],
  "service_tags": [],
  "amenities_tags": [],
  "dietary_tags": [],
  "service_model_tags": [],
  "price_range": null,
  "has_menu_link": null,
  "serves_alcohol_signal": null,
  "has_reservations": null,
  "offers_online_ordering": null,
  "offers_delivery": null,
  "offers_takeout": null,
  "offers_catering": null,
  "private_events_available": null,
  "has_happy_hour": null,
  "has_brunch": null,
  "has_breakfast": null,
  "outdoor_dining_signal": null,
  "live_music_signal": null,
  "dog_friendly_signal": null,
  "kid_friendly_signal": null,
  "dietary_options_signal": null,
  "restaurant_intelligence_notes": "",
  "confidence": 0,
  "reason": ""
}
"""
