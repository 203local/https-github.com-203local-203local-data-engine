from dataclasses import dataclass
from urllib.parse import urlparse

from app.discovery.scoring import score_website_candidate
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

    scored = []

    for result in results:
        if not result.url:
            continue

        if is_blocked(result.url):
            continue

        score = score_website_candidate(
            result,
            business_name,
            town,
        )

        scored.append((score, result))

    if scored:
        scored.sort(reverse=True, key=lambda x: x[0])
        best_score, best = scored[0]

        return WebsiteDiscoveryResult(
            website=best.url,
            confidence=min(best_score / 100.0, 1.0),
            reason=f"Highest scoring candidate ({best_score})",
        )

    return WebsiteDiscoveryResult(
        website="",
        confidence=0.0,
        reason="No suitable website found",
    )
