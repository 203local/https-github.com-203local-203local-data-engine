from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import socket

from app.website.html_parser import parse_website_html
from app.website.models import WebsiteData
from app.website.provider import WebsiteProvider


class RealWebsiteProvider(WebsiteProvider):
    def lookup(self, business_name, town, website=None):
        if not website:
            return WebsiteData()

        url = website if website.startswith("http") else f"https://{website}"

        try:
            request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(request, timeout=10) as response:
                html = response.read().decode("utf-8", errors="ignore")
        except (URLError, HTTPError, TimeoutError, socket.timeout, ValueError):
            return WebsiteData(website=website)

        parsed = parse_website_html(html, base_url=url)

        return WebsiteData(
            website=website,
            phone=parsed.get("phone"),
            email=parsed.get("email"),
            facebook=parsed.get("facebook"),
            instagram=parsed.get("instagram"),
        )
