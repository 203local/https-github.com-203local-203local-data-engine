def build_queries(business_name, town, state="CT"):
    return [
        f"{business_name} {town} {state}",
        f"{business_name} official website",
        f'"{business_name}"',
        f"{business_name} menu",
        f"{business_name} {town}",
    ]
