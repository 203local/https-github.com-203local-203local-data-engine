from urllib.parse import urlparse


HEAVILY_BLOCKED_DOMAINS = [
    "facebook.com",
    "instagram.com",
    "snapchat.com",
    "tiktok.com",
    "yelp.com",
    "tripadvisor.com",
    "ubereats.com",
    "grubhub.com",
    "doordash.com",
    "singleplatform.com",
    "eventective.com",
    "patch.com",
    "mapquest.com",
    "mindtrip.ai",
    "restaurantji.com",
    "opentable.com",
    "seamless.com",
    "toasttab.com",
    "ezcater.com",
    "foursquare.com",
    "yellowpages.com",
]


def normalize(value):
    return str(value or "").lower().strip()


def simplify(value):
    return (
        normalize(value)
        .replace("&", "and")
        .replace("'", "")
        .replace(".", "")
        .replace(",", "")
        .replace("-", "")
        .replace("_", "")
        .replace(" ", "")
    )


def score_website_candidate(result, business_name, town):
    score = 0

    business = normalize(business_name)
    business_simple = simplify(business_name)
    town_value = normalize(town)

    title = normalize(result.title)
    snippet = normalize(result.snippet)
    url = normalize(result.url)

    parsed = urlparse(result.url)
    domain = parsed.netloc.lower().replace("www.", "")
    domain_simple = simplify(domain)

    if any(blocked in domain for blocked in HEAVILY_BLOCKED_DOMAINS):
        score -= 80

    if business and business in title:
        score += 40

    if business_simple and business_simple in domain_simple:
        score += 60

    if business_simple and business_simple in simplify(url):
        score += 25

    if town_value and (town_value in title or town_value in snippet):
        score += 15

    if result.url.startswith("https://"):
        score += 10

    if domain.endswith((".com", ".net", ".org")):
        score += 10

    return score
