import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from app.search.models import SearchResult
from app.search.provider import SearchProvider


class TavilySearchProvider(SearchProvider):
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.disabled = False
        self.disable_reason = ""

    def search(self, query, limit=5):
        if self.disabled:
            return []

        if not self.api_key:
            self.disabled = True
            self.disable_reason = "API key is not configured"
            print("Tavily disabled: API key is not configured.")
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

            if error.code in {401, 402, 403, 429, 432}:
                self.disabled = True
                self.disable_reason = f"HTTP {error.code}"
                print(
                    f"Tavily disabled for this run after HTTP {error.code}. "
                    "Website discovery will continue without Tavily."
                )
                return []

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
