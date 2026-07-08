def expand_queries(business_name, town, state="CT"):
    queries = [
        f'{business_name} {town} {state}',
        f'"{business_name}" {town}',
        f'"{business_name}" official website',
        f'"{business_name}" menu',
        f'"{business_name}" contact',
        f'{business_name} restaurant {town}',
        f'{business_name} CT',
        f'{business_name} hours',
    ]

    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for query in queries:
        if query not in seen:
            seen.add(query)
            unique.append(query)

    return unique
