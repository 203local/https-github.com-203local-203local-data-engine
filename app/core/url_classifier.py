from urllib.parse import urlparse

OFFICIAL_BLOCKLIST = {
    "singleplatform.com",
    "places.singleplatform.com",
    "mappway.com",
    "twupro.com",
    "restaurantji.com",
    "allmenus.com",
    "menupix.com",
    "sirved.com",
    "yelp.com",
    "tripadvisor.com",
    "yellowpages.com",
    "mapquest.com",
}

SOCIAL_DOMAINS = {
    "facebook.com",
    "instagram.com",
    "tiktok.com",
    "linkedin.com",
    "x.com",
}

ORDERING_DOMAINS = {
    "toasttab.com",
    "order.toasttab.com",
    "slice.com",
    "clover.com",
    "chownow.com",
    "ubereats.com",
    "doordash.com",
    "grubhub.com",
}

def normalize(url):
    if not url:
        return ""

    if "://" not in url:
        url = "https://" + url

    domain = urlparse(url).netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain

def classify(url):
    domain = normalize(url)

    for blocked in OFFICIAL_BLOCKLIST:
        if domain.endswith(blocked):
            return "directory"

    for social in SOCIAL_DOMAINS:
        if domain.endswith(social):
            return "social"

    for ordering in ORDERING_DOMAINS:
        if domain.endswith(ordering):
            return "ordering"

    return "official"
from urllib.parse import urlparse


SOCIAL_DOMAINS = {
    "facebook.com",
    "instagram.com",
    "tiktok.com",
    "linkedin.com",
    "x.com",
    "twitter.com",
}

ORDERING_DOMAINS = {
    "toasttab.com",
    "order.toasttab.com",
    "clover.com",
    "chownow.com",
    "slice.com",
    "doordash.com",
    "ubereats.com",
    "grubhub.com",
    "seamless.com",
}

DIRECTORY_DOMAINS = {
    "yelp.com",
    "tripadvisor.com",
    "singleplatform.com",
    "places.singleplatform.com",
    "mappway.com",
    "twupro.com",
    "mapquest.com",
    "yellowpages.com",
    "restaurantji.com",
    "menupix.com",
    "allmenus.com",
    "sirved.com",
    "loc8nearme.com",
}

SEARCH_DOMAINS = {
    "google.com",
    "googleusercontent.com",
    "bing.com",
}


def normalize_domain(url):
    if not url:
        return ""

    value = str(url).strip().lower()

    if not value:
        return ""

    if "://" not in value:
        value = f"https://{value}"

    try:
        domain = urlparse(value).netloc.lower()
    except ValueError:
        return ""

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


def domain_matches(domain, known_domains):
    return any(
        domain == known
        or domain.endswith(f".{known}")
        for known in known_domains
    )


def classify_url(url):
    domain = normalize_domain(url)

    if not domain:
        return {
            "valid": False,
            "classification": "Invalid URL",
            "domain": "",
            "can_be_official_website": False,
        }

    if domain_matches(domain, SOCIAL_DOMAINS):
        classification = "Social Profile"
        can_be_official = False

    elif domain_matches(domain, ORDERING_DOMAINS):
        classification = "Ordering Platform"
        can_be_official = False

    elif domain_matches(domain, DIRECTORY_DOMAINS):
        classification = "Directory Listing"
        can_be_official = False

    elif domain_matches(domain, SEARCH_DOMAINS):
        classification = "Search Result"
        can_be_official = False

    else:
        classification = "Possible Official Website"
        can_be_official = True

    return {
        "valid": True,
        "classification": classification,
        "domain": domain,
        "can_be_official_website": can_be_official,
    }

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
