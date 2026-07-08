from app.google_business.models import GoogleBusinessData
from app.google_business.provider import GoogleBusinessProvider


class MockGoogleBusinessProvider(GoogleBusinessProvider):
    def search(self, business_name: str, town: str) -> GoogleBusinessData:
        return GoogleBusinessData(
            maps_url=None,
            rating=None,
            review_count=None,
            price_level=None,
            hours=None,
            categories=[],
            website=None,
            phone=None,
            status=None,
            source="mock",
        )
