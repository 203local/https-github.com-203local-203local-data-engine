from app.ai_enrichment.auto_enrich import run as run_ai_enrichment
from app.restaurant_intelligence.auto_enrich import run as run_restaurant_intelligence
from app.business_intelligence.auto_enrich import run as run_business_intelligence


JOBS = {
    "ai_enrichment": run_ai_enrichment,
    "restaurant_intelligence": run_restaurant_intelligence,
    "business_intelligence": run_business_intelligence,
}


def list_jobs():
    return sorted(JOBS.keys())


def get_job(name):
    return JOBS.get(name)
