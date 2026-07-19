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


DIRECTORY_PROVIDERS = {
    "singleplatform.com": "SinglePlatform",
    "twupro.com": "Twupro",
    "mappway.com": "Mappway",
    "yelp.com": "Yelp",
    "restaurantji.com": "Restaurantji",
    "yellowpages.com": "Yellow Pages",
    "mapquest.com": "MapQuest",
    "tripadvisor.com": "Tripadvisor",
    "foursquare.com": "Foursquare",
    "menupix.com": "MenuPix",
    "allmenus.com": "Allmenus",
    "loc8nearme.com": "Loc8NearMe",
    "superpages.com": "Superpages",
    "chamberofcommerce.com": "Chamber of Commerce",
}


SOCIAL_PROVIDERS = {
    "facebook.com": "Facebook",
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
    value = str(url or "").strip()

    if not value:
        return ""

    if "://" not in value:
        value = f"https://{value}"

    try:
        parsed = urlparse(value)
        hostname = (parsed.hostname or "").lower().strip(".")
        port = parsed.port
    except ValueError:
        return ""

    if not hostname:
        return ""

    if hostname.startswith("www."):
        hostname = hostname[4:]

    netloc = hostname

    if port and port not in {80, 443}:
        netloc = f"{hostname}:{port}"

    path = "/" + "/".join(
        part for part in parsed.path.split("/") if part
    )

    if path == "/":
        path = ""

    clean_query = []

    for key, item_value in parse_qsl(
        parsed.query,
        keep_blank_values=True,
    ):
        lowered_key = key.lower()

        if lowered_key.startswith("utm_"):
            continue

        if lowered_key in TRACKING_PARAMETERS:
            continue

        clean_query.append((key, item_value))

    query = urlencode(clean_query, doseq=True)

    return urlunparse(
        (
            "https",
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

    return (urlparse(canonical_url).hostname or "").lower()


def find_provider(domain: str, providers: dict) -> Optional[str]:
    for provider_domain, provider_name in providers.items():
        if (
            domain == provider_domain
            or domain.endswith(f".{provider_domain}")
        ):
            return provider_name

    return None


def classify_url(url: str) -> URLClassification:
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

    provider = find_provider(domain, DIRECTORY_PROVIDERS)

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

    provider = find_provider(domain, SOCIAL_PROVIDERS)

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
                "It should be stored as the primary online presence."
            ),
        )

    provider = find_provider(domain, ORDERING_PROVIDERS)

    if provider:
        return URLClassification(
            original_url=original_url,
            canonical_url=canonical_url,
            domain=domain,
            category="ordering",
            provider=provider,
            confidence=1.0,
            warning=(
                f"This appears to be a {provider} ordering page, "
                "not an official business website."
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
