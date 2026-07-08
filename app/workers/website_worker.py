from app.discovery.website_discovery import discover_official_website
from app.website.real_provider import RealWebsiteProvider
from app.workers.base_worker import BaseWorker, WorkerResult, WorkerUpdate


class WebsiteWorker(BaseWorker):
    name = "Website Worker"

    def __init__(self, provider=None):
        self.provider = provider or RealWebsiteProvider()

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
        existing_website = self.clean_text(row.get("website"))

        notes = []
        discovered_website = existing_website
        discovery_confidence = 1.0 if existing_website else 0.0

        if not discovered_website:
            discovery = discover_official_website(business_name, town)
            discovered_website = discovery.website
            discovery_confidence = discovery.confidence
            notes.append(discovery.reason)

        if not discovered_website or discovery_confidence < 0.70:
            return WorkerResult(
                worker_name=self.name,
                business_name=business_name,
                updates=[],
                status="skipped",
                notes=notes or ["No confident website discovered"],
            )

        data = self.provider.lookup(
            business_name,
            town,
            discovered_website,
        )

        updates = [
            WorkerUpdate("website", discovered_website, source="website_discovery", confidence=discovery_confidence),
            WorkerUpdate("phone", data.phone, source="website_scrape", confidence=0.80),
            WorkerUpdate("email", data.email, source="website_scrape", confidence=0.85),
            WorkerUpdate("facebook", data.facebook, source="website_scrape", confidence=0.80),
            WorkerUpdate("instagram", data.instagram, source="website_scrape", confidence=0.80),
        ]

        return WorkerResult(
            worker_name=self.name,
            business_name=business_name,
            updates=updates,
            status="success",
            notes=notes,
        )
