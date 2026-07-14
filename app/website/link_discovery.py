from html.parser import HTMLParser
from urllib.parse import urljoin


CONTACT_KEYWORDS = [
    "contact",
    "about",
    "location",
    "locations",
    "team",
    "staff",
]


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return

        href = dict(attrs).get("href")

        if href:
            self.links.append(href)


def discover_candidate_pages(html, base_url):
    if not html or not base_url:
        return []

    parser = LinkParser()

    try:
        parser.feed(html)
        parser.close()
    except (NotImplementedError, ValueError, TypeError):
        return []

    pages = []

    for href in parser.links:
        if not isinstance(href, str):
            continue

        href = href.strip()

        if not href:
            continue

        lower = href.lower()

        if any(keyword in lower for keyword in CONTACT_KEYWORDS):
            pages.append(urljoin(base_url, href))

    return list(dict.fromkeys(pages))
