import re
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from app.website.models import WebsiteData
from app.website.provider import WebsiteProvider


class RealWebsiteProvider(WebsiteProvider):
    def lookup(self, business_name, town, website=None):
        if not website:
            return WebsiteData()

        url = website if website.startswith("http") else f"https://{website}"

        try:
            request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(request, timeout=8) as response:
                html = response.read().decode("utf-8", errors="ignore")
        except (URLError, HTTPError, TimeoutError, ValueError):
            return WebsiteData(website=website)

        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", html)

        facebook = self.find_social(html, "facebook.com")
        instagram = self.find_social(html, "instagram.com")

        return WebsiteData(
            website=website,
            email=emails[0] if emails else None,
            facebook=facebook,
            instagram=instagram,
        )

    def find_social(self, html, domain):
        pattern = rf'https?://[^"\']*{re.escape(domain)}[^"\']*'
        matches = re.findall(pattern, html)

        if not matches:
            return None

        return matches[0].split("?")[0]
