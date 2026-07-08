from app.google_business.mock_provider import MockGoogleBusinessProvider
from app.workers.base_worker import BaseWorker, WorkerResult


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

        return WorkerResult(
            worker_name=self.name,
            business_name=business_name,
            updates=[],
            status="skipped",
            notes=[f"Provider source: {data.source}"],
        )
