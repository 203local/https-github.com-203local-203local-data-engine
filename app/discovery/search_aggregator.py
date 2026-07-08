from app.discovery.search_strategy import build_queries


def gather_results(provider, business_name, town):
    results = []

    for query in build_queries(business_name, town):
        try:
            search_results = provider.search(query, limit=5)
            results.extend(search_results)
        except Exception as error:
            print(f"Search failed for '{query}': {error}")

    return results
