from urllib.parse import quote_plus


def build_google_search_url(name, town="", state="CT"):
    query = f"{name} {town} {state} official website".strip()
    return "https://www.google.com/search?q=" + quote_plus(query)
