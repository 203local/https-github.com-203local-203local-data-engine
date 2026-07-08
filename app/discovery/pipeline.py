from app.discovery.deduplicate import deduplicate_results
from app.discovery.scoring import score_website_candidate
from app.discovery.search_aggregator import gather_results
from app.search.tavily_search import TavilySearchProvider


def discover_best_website_candidate(business_name, town):
    provider = TavilySearchProvider()

    raw_results = gather_results(provider, business_name, town)
    unique_results = deduplicate_results(raw_results)

    scored = []

    for result in unique_results:
        score = score_website_candidate(result, business_name, town)
        scored.append((score, result))

    scored.sort(reverse=True, key=lambda item: item[0])

    if not scored:
        return None, 0, []

    best_score, best_result = scored[0]

    return best_result, best_score, scored
