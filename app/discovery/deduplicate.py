from urllib.parse import urlparse


def normalize_url(url):
    url = (url or "").strip().lower()

    if url.startswith("https://"):
        url = url[8:]
    elif url.startswith("http://"):
        url = url[7:]

    if url.startswith("www."):
        url = url[4:]

    return url.rstrip("/")


def deduplicate_results(results):
    seen = set()
    unique = []

    for result in results:
        key = normalize_url(result.url)

        if key in seen:
            continue

        seen.add(key)
        unique.append(result)

    return unique
