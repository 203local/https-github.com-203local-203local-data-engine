from urllib.parse import urljoin
from html.parser import HTMLParser


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
    parser = LinkParser()
    parser.feed(html)

    pages = []

    for href in parser.links:
        lower = href.lower()

        if any(keyword in lower for keyword in CONTACT_KEYWORDS):
            pages.append(urljoin(base_url, href))

    return list(dict.fromkeys(pages))