from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import socket

from app.website.html_parser import parse_website_html
from app.website.link_discovery import discover_candidate_pages
from app.website.models import WebsiteData
from app.website.provider import WebsiteProvider


class RealWebsiteProvider(WebsiteProvider):
    def fetch_html(self, url):
        try:
            request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(request, timeout=10) as response:
                return response.read().decode("utf-8", errors="ignore")
        except (URLError, HTTPError, TimeoutError, socket.timeout, ValueError):
            return ""

    def lookup(self, business_name, town, website=None):
        if not website:
            return WebsiteData()

        url = website if website.startswith("http") else f"https://{website}"

        homepage_html = self.fetch_html(url)

        if not homepage_html:
            return WebsiteData(website=website)

        parsed = parse_website_html(homepage_html, base_url=url)

        candidate_pages = discover_candidate_pages(homepage_html, url)[:5]

        for page_url in candidate_pages:
            page_html = self.fetch_html(page_url)

            if not page_html:
                continue

            page_data = parse_website_html(page_html, base_url=page_url)

            for key, value in page_data.items():
                if not parsed.get(key) and value:
                    parsed[key] = value

        return WebsiteData(
            website=website,
            phone=parsed.get("phone"),
            email=parsed.get("email"),
            facebook=parsed.get("facebook"),
            instagram=parsed.get("instagram"),
        )
