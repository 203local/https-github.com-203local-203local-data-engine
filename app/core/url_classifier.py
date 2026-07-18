from urllib.parse import urlparse


SOCIAL_DOMAINS = {
    "facebook.com": "facebook",
    "www.facebook.com": "facebook",
    "instagram.com": "instagram",
    "www.instagram.com": "instagram",
}

ORDERING_DOMAINS = {
    "toasttab.com",
    "www.toasttab.com",
    "order.toasttab.com",
    "square.site",
    "www.squareup.com",
    "chownow.com",
    "www.chownow.com",
    "clover.com",
    "www.clover.com",
    "bentobox.com",
    "www.bentobox.com",
}

DIRECTORY_DOMAINS = {
    "singleplatform.com",
    "places.singleplatform.com",
    "mappway.com",
    "www.mappway.com",
    "allmenus.com",
    "www.allmenus.com",
    "menupix.com",
    "www.menupix.com",
    "restaurantguru.com",
    "www.restaurantguru.com",
    "yelp.com",
    "www.yelp.com",
    "tripadvisor.com",
    "www.tripadvisor.com",
}


def normalize_domain(url):
    value = str(url or "").strip()

    if not value:
        return ""

    if "://" not in value:
        value = f"https://{value}"

    parsed = urlparse(value)
    domain = parsed.netloc.lower().split(":")[0]

    return domain


def classify_url(url):
    domain = normalize_domain(url)

    if not domain:
        return "unknown"

    if domain in SOCIAL_DOMAINS:
        return SOCIAL_DOMAINS[domain]

    if domain in ORDERING_DOMAINS:
        return "ordering_platform"

    if domain in DIRECTORY_DOMAINS:
        return "directory_listing"

    if domain.endswith(".facebook.com"):
        return "facebook"

    if domain.endswith(".instagram.com"):
        return "instagram"

    if domain.endswith(".toasttab.com"):
        return "ordering_platform"

    if domain.endswith(".singleplatform.com"):
        return "directory_listing"

    if domain.endswith(".mappway.com"):
        return "directory_listing"

    return "official"
