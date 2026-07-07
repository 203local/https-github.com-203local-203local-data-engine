PLAYBOOKS = {
    "daily_refresh": {
        "name": "Daily Directory Refresh",
        "jobs": [
            "ai_enrichment",
            "restaurant_intelligence",
            "business_intelligence",
        ],
    },
    "restaurant_refresh": {
        "name": "Restaurant Refresh",
        "jobs": [
            "restaurant_intelligence",
            "business_intelligence",
        ],
    },
    "ai_only": {
        "name": "AI Enrichment Only",
        "jobs": [
            "ai_enrichment",
        ],
    },
}
