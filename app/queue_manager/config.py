from app.ai_enrichment.config import BATCH_FOLDER as AI_BATCH_FOLDER
from app.restaurant_intelligence.config import BATCH_FOLDER as RESTAURANT_BATCH_FOLDER
from app.business_intelligence.config import BATCH_FOLDER as BUSINESS_BATCH_FOLDER

QUEUES = {
    "ai_enrichment": {
        "folder": AI_BATCH_FOLDER,
        "pattern": "ai_batch_*.csv",
    },
    "restaurant_intelligence": {
        "folder": RESTAURANT_BATCH_FOLDER,
        "pattern": "restaurant_intelligence_batch_*.csv",
    },
    "business_intelligence": {
        "folder": BUSINESS_BATCH_FOLDER,
        "pattern": "business_intelligence_batch_*.csv",
    },
}
