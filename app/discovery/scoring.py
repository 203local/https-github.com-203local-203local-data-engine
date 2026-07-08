from urllib.parse import urlparse


BLOCKED_DOMAINS = [
    "facebook.com",
    "instagram.com",
    "yelp.com",
    "tripadvisor.com",
    "doordash.com",
    "ubereats.com",
    "grubhub.com",
    "opentable.com",
    "mapquest.com",
    "yellowpages.com",
]


def normalize(value):
    return str(value or "").lower().strip()


def score_website_candidate(result, business_name, town):
    score = 0

    business = normalize(business_name)
    town_value = normalize(town)
    title = normalize(result.title)
    snippet = normalize(result.snippet)
    url = normalize(result.url)

    domain = urlparse(result.url).netloc.lower()

    if any(blocked in domain for blocked in BLOCKED_DOMAINS):
        score -= 50

    if business and business in title:
        score += 40

    if business and business.replace(" ", "") in url.replace("-", "").replace("_", ""):
        score += 25

    if town_value and (town_value in title or town_value in snippet):
        score += 15

    if result.url.startswith("https://"):
        score += 10

    if domain.endswith((".com", ".net", ".org")):
        score += 10

    return score
