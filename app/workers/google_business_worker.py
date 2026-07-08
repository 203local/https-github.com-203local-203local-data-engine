from app.google_business.mock_provider import MockGoogleBusinessProvider
from app.workers.base_worker import BaseWorker, WorkerResult, WorkerUpdate


class GoogleBusinessWorker(BaseWorker):
    name = "Google Business Worker"

    def __init__(self, provider=None):
        self.provider = provider or MockGoogleBusinessProvider()

    def clean_text(self, value):
        if value is None:
            return ""
        if str(value).lower() == "nan":
            return ""
        return str(value).strip()

    def can_run(self, row):
        google_maps_url = self.clean_text(row.get("google_maps_url"))
        google_rating = self.clean_text(row.get("google_rating"))
        google_review_count = self.clean_text(row.get("google_review_count"))

        return not all([google_maps_url, google_rating, google_review_count])

    def run(self, row):
        business_name = self.clean_text(row.get("post_title"))
        town = self.clean_text(row.get("town"))

        data = self.provider.search(business_name, town)

        updates = [
            WorkerUpdate(
                field="google_maps_url",
                value=data.maps_url,
                source=data.source,
                confidence=0.95,
            ),
            WorkerUpdate(
                field="google_rating",
                value=data.rating,
                source=data.source,
                confidence=0.95,
            ),
            WorkerUpdate(
                field="google_review_count",
                value=data.review_count,
                source=data.source,
                confidence=0.95,
            ),
        ]

        return WorkerResult(
            worker_name=self.name,
            business_name=business_name,
            updates=updates,
            status="success",
            notes=[f"Provider source: {data.source}"],
        )
