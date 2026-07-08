from urllib.parse import urlparse

from app.discovery.deduplicate import deduplicate_results
from app.discovery.scoring import score_website_candidate
from app.discovery.search_aggregator import gather_results
from app.discovery.validation_scoring import score_validation
from app.discovery.website_validator import fetch_homepage
from app.search.tavily_search import TavilySearchProvider


NON_OFFICIAL_DOMAINS = [
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


def is_non_official(url):
    domain = urlparse(url).netloc.lower()
    return any(blocked in domain for blocked in NON_OFFICIAL_DOMAINS)


def discover_best_website_candidate(business_name, town, minimum_score=40):
    provider = TavilySearchProvider()

    raw_results = gather_results(provider, business_name, town)
    unique_results = deduplicate_results(raw_results)

    scored = []

    for result in unique_results:
        search_score = score_website_candidate(result, business_name, town)

        validation = fetch_homepage(result.url)
        validation_score = 0

        if validation.reachable:
            validation_score = score_validation(
                result.url,
                validation.html,
                business_name,
                town,
            )

        total_score = search_score + validation_score

        scored.append((total_score, result))

    scored.sort(reverse=True, key=lambda item: item[0])

    for score, result in scored:
        if score < minimum_score:
            continue

        if is_non_official(result.url):
            continue

        return result, score, scored

    return None, 0, scored
