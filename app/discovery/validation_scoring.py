from urllib.parse import urlparse


PUBLISHER_SIGNALS = [
    "news",
    "article",
    "author",
    "posted on",
    "published",
    "newspaper",
]

OFFICIAL_SIGNALS = [
    "contact",
    "about",
    "menu",
    "hours",
    "location",
    "reservations",
    "order online",
]


def normalize(value):
    return str(value or "").lower()


def score_validation(url, html, business_name, town):
    html_text = normalize(html)
    domain = urlparse(url).netloc.lower()

    score = 0

    if business_name.lower() in html_text:
        score += 25

    if town.lower() in html_text:
        score += 15

    for signal in OFFICIAL_SIGNALS:
        if signal in html_text:
            score += 5

    for signal in PUBLISHER_SIGNALS:
        if signal in html_text:
            score -= 10

    if any(word in domain for word in ["news", "patch", "register", "independent"]):
        score -= 50

    return score
