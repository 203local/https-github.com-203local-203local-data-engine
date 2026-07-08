from app.website.models import WebsiteData
from app.website.provider import WebsiteProvider


class MockWebsiteProvider(WebsiteProvider):
    def lookup(self, business_name, town):
        return WebsiteData(
            website=None,
            phone=None,
            email=None,
            facebook=None,
            instagram=None,
        )
