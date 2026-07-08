import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from app.search.models import SearchResult
from app.search.provider import SearchProvider


class GoogleCustomSearchProvider(SearchProvider):
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
        self.search_engine_id = os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_ID")

    def search(self, query, limit=5):
        if not self.api_key or not self.search_engine_id:
            print("Google Custom Search credentials are not configured.")
            return []

        params = urlencode({
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": min(limit, 10),
        })

        url = f"https://www.googleapis.com/customsearch/v1?{params}"

        try:
            with urlopen(url, timeout=15) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            body = error.read().decode("utf-8", errors="ignore")
            print(f"Google Custom Search HTTP error {error.code}:")
            print(body)
            return []
        except URLError as error:
            print(f"Google Custom Search URL error: {error}")
            return []

        results = []

        for item in payload.get("items", []):
            results.append(
                SearchResult(
                    query=query,
                    url=item.get("link", ""),
                    title=item.get("title", ""),
                    snippet=item.get("snippet", ""),
                    source="google_custom_search",
                    confidence=0.75,
                )
            )

        return results
