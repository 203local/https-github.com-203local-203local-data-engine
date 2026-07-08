from app.workers.google_business_worker import GoogleBusinessWorker
from app.workers.website_worker import WebsiteWorker
from app.workers.registry import registry


def register_default_workers():
    registry.register(GoogleBusinessWorker())
    registry.register(WebsiteWorker())
    return registry


register_default_workers()
