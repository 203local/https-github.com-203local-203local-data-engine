import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from app.search.models import SearchResult
from app.search.provider import SearchProvider


class TavilySearchProvider(SearchProvider):
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")

    def search(self, query, limit=5):
        if not self.api_key:
            print("Tavily API key is not configured.")
            return []

        payload = json.dumps({
            "api_key": self.api_key,
            "query": query,
            "search_depth": "basic",
            "max_results": limit,
        }).encode("utf-8")

        request = Request(
            "https://api.tavily.com/search",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=20) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            body = error.read().decode("utf-8", errors="ignore")
            print(f"Tavily HTTP error {error.code}:")
            print(body)
            return []
        except URLError as error:
            print(f"Tavily URL error: {error}")
            return []

        results = []

        for item in data.get("results", []):
            results.append(
                SearchResult(
                    query=query,
                    url=item.get("url", ""),
                    title=item.get("title", ""),
                    snippet=item.get("content", ""),
                    source="tavily",
                    confidence=item.get("score", 0.75),
                )
            )

        return results
