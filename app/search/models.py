from dataclasses import dataclass


@dataclass
class SearchResult:
    query: str
    url: str = ""
    title: str = ""
    snippet: str = ""
    source: str = ""
    confidence: float = 0.0
