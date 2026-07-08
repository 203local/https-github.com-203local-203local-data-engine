from app.website.mock_provider import MockWebsiteProvider
from app.workers.base_worker import BaseWorker, WorkerResult, WorkerUpdate


class WebsiteWorker(BaseWorker):
    name = "Website Worker"

    def __init__(self, provider=None):
        self.provider = provider or MockWebsiteProvider()

    def clean_text(self, value):
        if value is None:
            return ""
        if str(value).lower() == "nan":
            return ""
        return str(value).strip()

    def can_run(self, row):
        fields_to_check = [
            "website",
            "phone",
            "email",
            "facebook",
            "instagram",
        ]

        return any(not self.clean_text(row.get(field)) for field in fields_to_check)

    def run(self, row):
        business_name = self.clean_text(row.get("post_title"))
        town = self.clean_text(row.get("town"))

        data = self.provider.lookup(business_name, town)

        updates = [
            WorkerUpdate("website", data.website, source="website_provider", confidence=0.85),
            WorkerUpdate("phone", data.phone, source="website_provider", confidence=0.85),
            WorkerUpdate("email", data.email, source="website_provider", confidence=0.85),
            WorkerUpdate("facebook", data.facebook, source="website_provider", confidence=0.85),
            WorkerUpdate("instagram", data.instagram, source="website_provider", confidence=0.85),
        ]

        return WorkerResult(
            worker_name=self.name,
            business_name=business_name,
            updates=updates,
            status="success",
            notes=["Provider source: mock"],
        )
