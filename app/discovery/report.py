from app.discovery.deduplicate import deduplicate_results
from app.discovery.query_expansion import expand_queries
from app.discovery.scoring import score_website_candidate
from app.search.tavily_search import TavilySearchProvider


def run(business_name, town):
    provider = TavilySearchProvider()

    print()
    print("=" * 75)
    print(f"Discovery Report: {business_name}")
    print("=" * 75)
    print(f"Town: {town}")
    print()

    queries = expand_queries(business_name, town)

    print("Searches Executed")
    print("-" * 75)

    all_results = []

    for query in queries:
        print(f"✓ {query}")
        results = provider.search(query, limit=5)
        all_results.extend(results)

    unique_results = deduplicate_results(all_results)

    scored = []

    for result in unique_results:
        score = score_website_candidate(result, business_name, town)
        scored.append((score, result))

    scored.sort(reverse=True, key=lambda item: item[0])

    print()
    print("Candidates")
    print("-" * 75)

    if not scored:
        print("No candidates found.")
        return

    for score, result in scored[:15]:
        print(f"{score:>4}  {result.title}")
        print(f"      {result.url}")

    best_score, best = scored[0]

    print()
    print("Winner")
    print("-" * 75)
    print(f"Score: {best_score}")
    print(f"Title: {best.title}")
    print(f"URL:   {best.url}")
