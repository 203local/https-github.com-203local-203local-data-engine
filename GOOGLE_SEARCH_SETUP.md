# Google Custom Search Setup

The Website Worker uses Google Custom Search to discover official business websites.

Required environment variables:

GOOGLE_CUSTOM_SEARCH_API_KEY
GOOGLE_CUSTOM_SEARCH_ENGINE_ID

Example:

export GOOGLE_CUSTOM_SEARCH_API_KEY="your_api_key_here"
export GOOGLE_CUSTOM_SEARCH_ENGINE_ID="your_search_engine_id_here"

Test command:

python3 - <<'PY'
from app.search.google_custom_search import GoogleCustomSearchProvider

provider = GoogleCustomSearchProvider()
results = provider.search(
    "Copper City Bar & Grill Ansonia CT official website",
    limit=3,
)

for result in results:
    print(result.title)
    print(result.url)
    print()
PY
