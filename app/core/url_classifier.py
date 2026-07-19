from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


@dataclass(frozen=True)
class URLClassification:
    original_url: str
    canonical_url: str
    domain: str
    category: str
    provider: Optional[str]
    confidence: float
    warning: Optional[str]

    @property
    def is_official(self) -> bool:
        return self.category == "official"

    @property
    def requires_warning(self) -> bool:
        return self.category in {"directory", "ordering", "social", "invalid"}


DIRECTORY_PROVIDERS = {
    "singleplatform.com": "SinglePlatform",
    "places.singleplatform.com": "SinglePlatform",
    "restaurantji.com": "Restaurantji",
    "yelp.com": "Yelp",
    "m.yelp.com": "Yelp",
    "mappway.com": "Mappway",
    "twupro.com": "Twupro",
    "mapquest.com": "MapQuest",
    "yellowpages.com": "Yellow Pages",
    "tripadvisor.com": "Tripadvisor",
    "foursquare.com": "Foursquare",
    "chamberofcommerce.com": "Chamber of Commerce",
    "menupix.com": "MenuPix",
    "allmenus.com": "Allmenus",
    "loc8nearme.com": "Loc8NearMe",
    "superpages.com": "Superpages",
    "merchantcircle.com": "MerchantCircle",
    "nextdoor.com": "Nextdoor",
}


SOCIAL_PROVIDERS = {
    "facebook.com": "Facebook",
    "m.facebook.com": "Facebook",
    "instagram.com": "Instagram",
    "tiktok.com": "TikTok",
    "linkedin.com": "LinkedIn",
    "x.com": "X",
    "twitter.com": "X",
    "youtube.com": "YouTube",
    "youtu.be": "YouTube",
    "pinterest.com": "Pinterest",
    "threads.net": "Threads",
}


ORDERING_PROVIDERS = {
    "toasttab.com": "Toast",
    "order.toasttab.com": "Toast",
    "slice.com": "Slice",
    "slicelife.com": "Slice",
    "doordash.com": "DoorDash",
    "ubereats.com": "Uber Eats",
    "grubhub.com": "Grubhub",
    "chownow.com": "ChowNow",
    "seamless.com": "Seamless",
    "beyondmenu.com": "Beyond Menu",
    "clover.com": "Clover",
    "order.online": "Order Online",
    "square.site": "Square",
    "squareup.com": "Square",
    "foodbooking.com": "FoodBooking",
    "delivery.com": "Delivery.com",
    "ezcater.com": "ezCater",
}


TRACKING_PARAMETERS = {
    "fbclid",
    "gclid",
    "msclkid",
    "mc_cid",
    "mc_eid",
    "ref",
    "source",
}


def normalize_url(url: str) -> str:
    """Return a clean, canonical version of a URL."""
    value = str(url or "").strip()

    if not value:
        return ""

    if "://" not in value:
        value = f"https://{value}"

    try:
        parsed = urlparse(value)
    except ValueError:
        return ""

    if not parsed.netloc:
        return ""

    scheme = "https"
    hostname = (parsed.hostname or "").lower().strip(".")

    if not hostname:
        return ""

    if hostname.startswith("www."):
        hostname = hostname[4:]

    port = parsed.port
    netloc = hostname

    if port and port not in {80, 443}:
        netloc = f"{hostname}:{port}"

    path = parsed.path or ""
    path = "/" + "/".join(part for part in path.split("/") if part)

    if path == "/":
        path = ""

    clean_query_items = []

    for key, value in parse_qsl(parsed.query, keep_blank_values=True):
        lowered_key = key.lower()

        if lowered_key.startswith("utm_"):
            continue

        if lowered_key in TRACKING_PARAMETERS:
            continue

        clean_query_items.append((key, value))

    query = urlencode(clean_query_items, doseq=True)

    return urlunparse(
        (
            scheme,
            netloc,
            path,
            "",
            query,
            "",
        )
    )


def extract_domain(url: str) -> str:
    canonical_url = normalize_url(url)

    if not canonical_url:
        return ""

    parsed = urlparse(canonical_url)
    return (parsed.hostname or "").lower()


def _find_provider(
    domain: str,
    providers: dict[str, str],
) -> Optional[str]:
    for provider_domain, provider_name in providers.items():
        if domain == provider_domain or domain.endswith(f".{provider_domain}"):
            return provider_name

    return None


def classify_url(url: str) -> URLClassification:
    """Classify a URL as official, directory, ordering, social, or invalid."""
    original_url = str(url or "").strip()
    canonical_url = normalize_url(original_url)
    domain = extract_domain(canonical_url)

    if not canonical_url or not domain:
        return URLClassification(
            original_url=original_url,
            canonical_url="",
            domain="",
            category="invalid",
            provider=None,
            confidence=1.0,
            warning="The entered value is not a valid URL.",
        )

    provider = _find_provider(domain, DIRECTORY_PROVIDERS)

    if provider:
        return URLClassification(
            original_url=original_url,
            canonical_url=canonical_url,
            domain=domain,
            category="directory",
            provider=provider,
            confidence=1.0,
            warning=(
                f"This appears to be a {provider} directory listing, "
                "not an official business website."
            ),
        )

    provider = _find_provider(domain, SOCIAL_PROVIDERS)

    if provider:
        return URLClassification(
            original_url=original_url,
            canonical_url=canonical_url,
            domain=domain,
            category="social",
            provider=provider,
            confidence=1.0,
            warning=(
                f"This appears to be a {provider} profile. "
                "It should be stored as a primary online presence, "
                "not as the official website."
            ),
        )

    provider = _find_provider(domain, ORDERING_PROVIDERS)

    if provider:
        return URLClassification(
            original_url=original_url,
            canonical_url=canonical_url,
            domain=domain,
            category="ordering",
            provider=provider,
            confidence=1.0,
            warning=(
                f"This appears to be a {provider} ordering page. "
                "It should not normally replace the official website."
            ),
        )

    return URLClassification(
        original_url=original_url,
        canonical_url=canonical_url,
        domain=domain,
        category="official",
        provider=None,
        confidence=0.85,
        warning=None,
    )

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
