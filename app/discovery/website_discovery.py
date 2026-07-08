from dataclasses import dataclass
from urllib.parse import urlparse

from app.search.google_custom_search import GoogleCustomSearchProvider


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


@dataclass
class WebsiteDiscoveryResult:
    website: str = ""
    confidence: float = 0.0
    reason: str = ""


def is_blocked(url):
    domain = urlparse(url).netloc.lower()
    return any(blocked in domain for blocked in BLOCKED_DOMAINS)


def discover_official_website(business_name, town, state="CT"):
    query = f"{business_name} {town} {state} official website"

    provider = GoogleCustomSearchProvider()
    results = provider.search(query, limit=5)

    for result in results:
        if not result.url:
            continue

        if is_blocked(result.url):
            continue

        return WebsiteDiscoveryResult(
            website=result.url,
            confidence=0.75,
            reason="First non-blocked search result",
        )

    return WebsiteDiscoveryResult(
        website="",
        confidence=0.0,
        reason="No suitable website found",
    )
