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


def extract_social_links(html):
    links = {}

    for name, domain in SOCIAL_DOMAINS.items():
        pattern = rf'https?://[^"\']*{re.escape(domain)}[^"\']*'
        matches = re.findall(pattern, html or "")

        if matches:
            links[name] = matches[0].split("?")[0]

    return links


def extract_mailto_links(html):
    pattern = r'mailto:([^"\'>\s]+)'
    return sorted(set(re.findall(pattern, html or "")))


def extract_tel_links(html):
    pattern = r'tel:([^"\'>\s]+)'
    return sorted(set(re.findall(pattern, html or "")))


def parse_website_html(html, base_url=""):
    emails = extract_emails(html)
    mailto_emails = extract_mailto_links(html)
    phones = extract_phone_numbers(html)
    tel_numbers = extract_tel_links(html)
    socials = extract_social_links(html)

    return {
        "email": mailto_emails[0] if mailto_emails else (emails[0] if emails else None),
        "phone": tel_numbers[0] if tel_numbers else (phones[0] if phones else None),
        "facebook": socials.get("facebook"),
        "instagram": socials.get("instagram"),
        "tiktok": socials.get("tiktok"),
        "linkedin": socials.get("linkedin"),
        "youtube": socials.get("youtube"),
    }
