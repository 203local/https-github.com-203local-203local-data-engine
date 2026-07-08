from app.workers.google_business_worker import GoogleBusinessWorker
from app.workers.registry import registry


def register_default_workers():
    registry.register(GoogleBusinessWorker())
    return registry
