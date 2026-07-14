import re
from urllib.parse import urljoin


SOCIAL_DOMAINS = {
    "facebook": "facebook.com",
    "instagram": "instagram.com",
    "tiktok": "tiktok.com",
    "linkedin": "linkedin.com",
    "youtube": "youtube.com",
}


def extract_emails(html):
    return sorted(set(
        re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            html or "",
        )
    ))


def extract_phone_numbers(html):
    pattern = r"(?:\+1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
    return sorted(set(re.findall(pattern, html or "")))


def extract_social_links(html, preferred_location=""):
    links = {}
    normalized_location = re.sub(
        r"[^a-z0-9]",
        "",
        str(preferred_location).casefold(),
    )

    for name, domain in SOCIAL_DOMAINS.items():
        pattern = rf'https?://[^"\']*{re.escape(domain)}[^"\']*'
        matches = re.findall(pattern, html or "")

        cleaned_matches = list(dict.fromkeys(
            match.split("?")[0].rstrip("\\/")
            for match in matches
            if match
        ))

        if not cleaned_matches:
            continue

        if name == "facebook" and normalized_location:
            location_match = next(
                (
                    candidate
                    for candidate in cleaned_matches
                    if normalized_location
                    in re.sub(
                        r"[^a-z0-9]",
                        "",
                        candidate.casefold(),
                    )
                ),
                None,
            )

            if location_match:
                links[name] = location_match
                continue

        links[name] = cleaned_matches[0]

    return links


def extract_mailto_links(html):
    pattern = r'mailto:([^"\'>\s]+)'
    return sorted(set(re.findall(pattern, html or "")))


def extract_tel_links(html):
    pattern = r'tel:([^"\'>\s]+)'
    return sorted(set(re.findall(pattern, html or "")))


def parse_website_html(
    html,
    base_url="",
    preferred_location="",
):
    emails = extract_emails(html)
    mailto_emails = extract_mailto_links(html)
    phones = extract_phone_numbers(html)
    tel_numbers = extract_tel_links(html)
    socials = extract_social_links(
        html,
        preferred_location=preferred_location,
    )

    return {
        "email": mailto_emails[0] if mailto_emails else (emails[0] if emails else None),
        "phone": tel_numbers[0] if tel_numbers else (phones[0] if phones else None),
        "facebook": socials.get("facebook"),
        "instagram": socials.get("instagram"),
        "tiktok": socials.get("tiktok"),
        "linkedin": socials.get("linkedin"),
        "youtube": socials.get("youtube"),
    }
