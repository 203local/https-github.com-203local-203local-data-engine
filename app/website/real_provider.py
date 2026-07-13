import http.client
import re
import socket
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from app.website.html_parser import parse_website_html
from app.website.link_discovery import discover_candidate_pages
from app.website.models import WebsiteData
from app.website.provider import WebsiteProvider


class RealWebsiteProvider(WebsiteProvider):
    LOCATION_SPECIFIC_FIELDS = {
        "phone",
        "email",
        "facebook",
    }

    BRAND_LEVEL_FIELDS = {
        "instagram",
    }

    @staticmethod
    def normalize_url(url):
        if not url:
            return ""

        try:
            parts = urlsplit(str(url).strip())

            if parts.scheme not in {"http", "https"}:
                return ""

            if not parts.netloc:
                return ""

            safe_path = quote(
                parts.path,
                safe="/:@-._~!$&'()*+,;=%",
            )
            safe_query = quote(
                parts.query,
                safe="=&:@/?-._~!$'()*+,;%",
            )

            return urlunsplit(
                (
                    parts.scheme,
                    parts.netloc,
                    safe_path,
                    safe_query,
                    "",
                )
            )
        except (TypeError, ValueError):
            return ""

    def fetch_html(self, url):
        normalized_url = self.normalize_url(url)

        if not normalized_url:
            return ""

        try:
            request = Request(
                normalized_url,
                headers={"User-Agent": "Mozilla/5.0"},
            )

            with urlopen(request, timeout=10) as response:
                return response.read().decode(
                    "utf-8",
                    errors="ignore",
                )

        except (
            URLError,
            HTTPError,
            TimeoutError,
            socket.timeout,
            ValueError,
            http.client.InvalidURL,
            http.client.IncompleteRead,
            ConnectionResetError,
            ConnectionAbortedError,
            BrokenPipeError,
        ):
            return ""

    @staticmethod
    def normalize_text(value):
        if not value:
            return ""

        normalized = str(value).casefold()
        normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)
        normalized = re.sub(r"\s+", " ", normalized)

        return normalized.strip()

    def text_mentions_town(self, text, town):
        normalized_text = self.normalize_text(text)
        normalized_town = self.normalize_text(town)

        if not normalized_text or not normalized_town:
            return False

        return normalized_town in normalized_text

    def url_mentions_town(self, url, town):
        if not url or not town:
            return False

        parsed_url = urlparse(url)

        searchable_url = " ".join(
            [
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.query,
            ]
        )

        return self.text_mentions_town(
            searchable_url,
            town,
        )

    def page_matches_location(self, page_url, page_html, town, street):
        if not town and not street:
            return True

        if town:
            if self.url_mentions_town(page_url, town):
                return True

            if self.text_mentions_town(page_html, town):
                return True

        if street and self.text_mentions_town(page_html, street):
            return True

        return False

    def email_matches_location(self, email, town, street, page_html):
        if not email:
            return False

        local_part = email.split("@", 1)[0]

        if town and self.text_mentions_town(local_part, town):
            return True

        if town and self.text_mentions_town(page_html, town):
            return True

        if street and self.text_mentions_town(page_html, street):
            return True

        return False

    def merge_page_data(
        self,
        parsed,
        page_data,
        page_url,
        page_html,
        town,
        street,
    ):
        location_matches = self.page_matches_location(
            page_url,
            page_html,
            town,
            street,
        )

        for key, value in page_data.items():
            if not value:
                continue

            if parsed.get(key):
                continue

            if key in self.LOCATION_SPECIFIC_FIELDS:
                if not location_matches:
                    continue

                if key == "email":
                    if not self.email_matches_location(
                        value,
                        town,
                        street,
                        page_html,
                    ):
                        continue

                parsed[key] = value
                continue

            if key in self.BRAND_LEVEL_FIELDS:
                parsed[key] = value
                continue

            parsed[key] = value

    def lookup(
        self,
        business_name,
        town,
        street,
        website=None,
    ):
        if not website:
            return WebsiteData()

        url = (
            website
            if website.startswith("http")
            else f"https://{website}"
        )

        homepage_html = self.fetch_html(url)

        if not homepage_html:
            return WebsiteData(
                website=website,
            )

        homepage_data = parse_website_html(
            homepage_html,
            base_url=url,
        )

        parsed = {}

        self.merge_page_data(
            parsed=parsed,
            page_data=homepage_data,
            page_url=url,
            page_html=homepage_html,
            town=town,
            street=street,
        )

        candidate_pages = discover_candidate_pages(
            homepage_html,
            url,
        )[:5]

        for page_url in candidate_pages:
            page_html = self.fetch_html(page_url)

            if not page_html:
                continue

            page_data = parse_website_html(
                page_html,
                base_url=page_url,
            )

            self.merge_page_data(
                parsed=parsed,
                page_data=page_data,
                page_url=page_url,
                page_html=page_html,
                town=town,
                street=street,
            )

        return WebsiteData(
            website=url,
            phone=parsed.get("phone"),
            email=parsed.get("email"),
            facebook=parsed.get("facebook"),
            instagram=parsed.get("instagram"),
        )
